// Request types
export interface GenerateRequest {
  input: string;
  context?: string;
  platforms?: string[];
  options?: {
    include_assumptions?: boolean;
  };
}

// Analysis service types
export interface AnalysisResponse {
  request_id: string;
  original_text: string;
  intent: {
    primary: string;
    confidence: number;
    secondary: [string, number][];
  };
  entities: Array<{
    type: string;
    value: string;
    confidence: number;
  }>;
  placeholders: Array<{
    name: string;
    type: string;
    description: string;
    required: boolean;
    default?: string;
  }>;
  assumptions: Array<{
    category: string;
    value: string;
    confidence: number;
    reasoning: string;
  }>;
  processing_time_ms: number;
}

// Generation service types
export interface GeneratedPrompt {
  platform: string;
  platform_name: string;
  prompt: string;
  placeholders: Array<{
    key: string;
    name: string;
    description: string;
  }>;
  settings: Record<string, any>;
}

export interface GenerationResponse {
  request_id: string;
  intent: string;
  prompts: Record<string, GeneratedPrompt>;
  assumptions: Array<{
    category: string;
    value: string;
    confidence: number;
    reasoning: string;
  }>;
  processing_time_ms: number;
}

// Final API response
export interface PromptBundleResponse {
  id: string;
  input: string;
  analysis: {
    intent: string;
    confidence: number;
    entities: Array<{
      type: string;
      value: string;
    }>;
  };
  prompts: Record<string, {
    prompt: string;
    placeholders: Array<{
      key: string;
      description: string;
    }>;
    settings: Record<string, any>;
  }>;
  placeholders: Array<{
    name: string;
    description: string;
    required: boolean;
  }>;
  assumptions: Array<{
    category: string;
    value: string;
    reasoning: string;
  }>;
  metadata: {
    processing_time_ms: number;
    platforms_generated: string[];
    timestamp: string;
  };
}