/// <reference types="vite/client" />

interface ImportMetaEnv {
    readonly VITE_MAX_EVENTS_TO_DISPLAY: string
    // more env variables...
}

interface ImportMeta {
    readonly env: ImportMetaEnv
}
