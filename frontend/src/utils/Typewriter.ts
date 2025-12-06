/**
 * Variable-Speed Typewriter Buffer
 * Eliminates UI jitter by buffering incoming text and streaming it smoothly.
 * 
 * Logic:
 * - Incoming text is pushed to a queue.
 * - A "consumer" loop pulls characters from the queue.
 * - Speed is proportional to queue length:
 *   - Long queue -> Fast typing (catch up)
 *   - Short queue -> Slow typing (smooth finish)
 */

export class Typewriter {
    private queue: string[] = [];
    private currentText: string = '';
    private onUpdate: (text: string) => void;
    private targetBufferLength: number = 50; // Ideal buffer size
    private baseSpeed: number = 30; // Characters per second
    private lastFrameTime: number = 0;
    private accumulator: number = 0;
    private animationFrameId: number | null = null;

    constructor(onUpdate: (text: string) => void) {
        this.onUpdate = onUpdate;
    }

    /**
     * Add new text to the buffer.
     * @param text The new chunk of text to append
     */
    public push(text: string) {
        // Split into characters for smoother granularity
        this.queue.push(...text.split(''));
        if (!this.animationFrameId) {
            this.start();
        }
    }

    private start() {
        this.lastFrameTime = performance.now();
        this.loop();
    }

    private loop = () => {
        if (this.queue.length === 0) {
            this.animationFrameId = null;
            return;
        }

        const now = performance.now();
        const dt = (now - this.lastFrameTime) / 1000; // seconds
        this.lastFrameTime = now;

        // Calculate dynamic speed
        // Speed = Base * (CurrentLength / TargetLength)
        // We clamp the multiplier to avoid being too slow or insanely fast
        const bufferRatio = Math.max(0.5, this.queue.length / this.targetBufferLength);
        const currentSpeed = this.baseSpeed * bufferRatio * 2; // *2 factor to be responsive

        // Accumulate characters to print
        this.accumulator += currentSpeed * dt;

        let charsToPrint = Math.floor(this.accumulator);

        if (charsToPrint > 0) {
            // Don't print more than we have
            charsToPrint = Math.min(charsToPrint, this.queue.length);

            const chunk = this.queue.splice(0, charsToPrint).join('');
            this.currentText += chunk;
            this.onUpdate(this.currentText);

            this.accumulator -= charsToPrint;
        }

        this.animationFrameId = requestAnimationFrame(this.loop);
    }

    public reset() {
        this.queue = [];
        this.currentText = '';
        if (this.animationFrameId) {
            cancelAnimationFrame(this.animationFrameId);
            this.animationFrameId = null;
        }
    }

    public getCurrentText(): string {
        return this.currentText;
    }

    public flush() {
        if (this.queue.length > 0) {
            const chunk = this.queue.join('');
            this.currentText += chunk;
            this.queue = [];
            this.onUpdate(this.currentText);
        }
    }
}
