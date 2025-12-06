/**
 * Adaptive Cost Estimator
 * Implements a simplified Kalman Filter to estimate and smooth session costs in real-time.
 * 
 * Logic:
 * - Maintains an internal estimate of the cost.
 * - Projects cost forward based on estimated token generation rate.
 * - Corrects estimate when actual data arrives from backend.
 * - Adapts to "Thinking" vs "Generating" states.
 */

export class CostEstimator {
    private estimatedCost: number = 0;
    private lastUpdateTime: number = Date.now();
    private tokensPerSecond: number = 0;
    private processVariance: number = 0.001; // Process noise (how much we trust our projection)
    private measurementVariance: number = 0.01; // Measurement noise (how much we trust the backend update)
    private estimationError: number = 1.0;

    // Model specific rates (USD per 1k tokens) - approximate defaults
    private readonly MODEL_RATES: Record<string, { input: number; output: number }> = {
        'claude-3-5-sonnet-20241022': { input: 0.003, output: 0.015 },
        'claude-3-opus-20240229': { input: 0.015, output: 0.075 },
        'claude-3-haiku-20240307': { input: 0.00025, output: 0.00125 },
        'default': { input: 0.003, output: 0.015 }
    };

    private currentModel: string = 'default';
    private isThinking: boolean = false;

    constructor(initialCost: number = 0, model: string = 'default') {
        this.estimatedCost = initialCost;
        this.currentModel = model;
    }

    /**
     * Update the estimator with a new actual measurement from the backend.
     * @param measuredCost The actual cost reported by the API
     */
    public updateMeasurement(measuredCost: number) {
        // Kalman Gain Calculation
        const kalmanGain = this.estimationError / (this.estimationError + this.measurementVariance);

        // Update Estimate
        this.estimatedCost = this.estimatedCost + kalmanGain * (measuredCost - this.estimatedCost);

        // Update Error Covariance
        this.estimationError = (1 - kalmanGain) * this.estimationError;

        // Recalculate rate based on change since last update
        const now = Date.now();
        const dt = (now - this.lastUpdateTime) / 1000;
        if (dt > 0 && measuredCost > this.estimatedCost) {
            // Simple rate adjustment (could be filtered too)
            // This is a simplified approach to update the "velocity" of cost
        }
        this.lastUpdateTime = now;
    }

    /**
     * Project the cost forward in time (predict step).
     * Call this in your animation loop (e.g. requestAnimationFrame).
     * @param dtSeconds Delta time in seconds since last frame
     */
    public predict(dtSeconds: number): number {
        if (this.isThinking) {
            // Cost doesn't increase during thinking (usually, unless billing for thinking tokens)
            // For now assume thinking is free or billed as output later
            return this.estimatedCost;
        }

        // Project forward: Cost(t+1) = Cost(t) + Rate * dt
        // We estimate rate based on model pricing and an assumed speed (e.g. 50 tokens/s)
        // In a real implementation, we'd measure tokens/s dynamically.
        // For this MVP, we'll use a heuristic based on the model.

        const estimatedTokensPerSec = 30; // Conservative guess
        const rate = (this.MODEL_RATES[this.currentModel] || this.MODEL_RATES['default']).output / 1000 * estimatedTokensPerSec;

        this.estimatedCost += rate * dtSeconds;

        // Increase uncertainty over time without measurement
        this.estimationError += this.processVariance * dtSeconds;

        return this.estimatedCost;
    }

    public setThinking(thinking: boolean) {
        this.isThinking = thinking;
    }

    public setModel(model: string) {
        this.currentModel = model;
    }

    public getEstimate(): number {
        return this.estimatedCost;
    }
}
