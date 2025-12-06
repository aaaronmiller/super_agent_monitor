export * from './theme';

export type TimeRange = '1m' | '3m' | '5m' | '10m';

export interface ChartConfig {
    maxDataPoints: number;
    animationDuration: number;
    barWidth: number;
    barGap: number;
    colors: {
        primary: string;
        glow: string;
        axis: string;
        text: string;
    };
}

export interface HumanInTheLoopResponse {
    response?: string;
    permission?: boolean;
    choice?: string;
    hookEvent: HookEvent;
    respondedAt: number;
}

export interface HookEvent {
    id: string;
    hook_event_type: string;
    source_app: string;
    session_id: string;
    timestamp: number;
    payload: any;
    summary?: string;
    model_name?: string;
    model?: string;
    tool_name?: string;
    tool_command?: string;
    tool_file?: { path: string };
    tool_input?: any;
    humanInTheLoop?: {
        type: 'question' | 'permission' | 'choice';
        question?: string;
        choices?: string[];
    };
    humanInTheLoopStatus?: {
        status: 'pending' | 'responded';
        response?: HumanInTheLoopResponse;
    };
    chat?: any[];
    hitl_question?: string;
    hitl_permission?: string;
}

export interface FilterOptions {
    source_apps: string[];
    session_ids: string[];
    hook_event_types: string[];
}

export interface WebSocketMessage {
    type: 'initial' | 'event' | 'summary-update';
    data: any;
}
