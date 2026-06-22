/**
 * useVisualizationSettings.ts
 * 
 * Composable for managing toggleable visualization enhancement features.
 * These features extend the base Disler UI with Super Agent Monitor-specific data.
 */

import { ref, watch } from 'vue';

export interface VisualizationSettings {
    /** Show council type badge (🏛️/⚔️/🔄) on agent tags */
    showCouncilIndicator: boolean;
    /** Show E2B/Local runtime status indicator */
    showE2BStatus: boolean;
    /** Show cost sparkline in header */
    showCostSparkline: boolean;
    /** Show RAG injection indicator on agents */
    showRagIndicator: boolean;
    /** Show token flow overlay on pulse chart */
    showTokenFlowOverlay: boolean;
}

const STORAGE_KEY = 'sam-visualization-settings';

const defaultSettings: VisualizationSettings = {
    showCouncilIndicator: true,
    showE2BStatus: true,
    showCostSparkline: true,
    showRagIndicator: true,
    showTokenFlowOverlay: false, // Off by default (advanced)
};

// Load from localStorage or use defaults
const loadSettings = (): VisualizationSettings => {
    try {
        const stored = localStorage.getItem(STORAGE_KEY);
        if (stored) {
            return { ...defaultSettings, ...JSON.parse(stored) };
        }
    } catch (e) {
        console.warn('Failed to load visualization settings:', e);
    }
    return { ...defaultSettings };
};

// Singleton state
const settings = ref<VisualizationSettings>(loadSettings());

// Persist on change
watch(settings, (newSettings) => {
    try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(newSettings));
    } catch (e) {
        console.warn('Failed to save visualization settings:', e);
    }
}, { deep: true });

export function useVisualizationSettings() {
    const toggleSetting = (key: keyof VisualizationSettings) => {
        settings.value[key] = !settings.value[key];
    };

    const setSetting = (key: keyof VisualizationSettings, value: boolean) => {
        settings.value[key] = value;
    };

    const resetToDefaults = () => {
        settings.value = { ...defaultSettings };
    };

    return {
        settings,
        toggleSetting,
        setSetting,
        resetToDefaults,
    };
}
