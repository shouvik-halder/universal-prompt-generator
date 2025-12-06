import { v4 as uuidv4 } from 'uuid';
import { analyzeText } from '../services/analysisClient';
import { generatePrompts } from '../services/generationClient';
import { GenerateRequest, PromptBundleResponse } from '../models';

export async function orchestrate(request: GenerateRequest): Promise<PromptBundleResponse> {
  const startTime = Date.now();
  const requestId = `upg_${uuidv4().replace(/-/g, '').slice(0, 12)}`;

  // Step 1: Analyze the input
  const analysis = await analyzeText(request.input, request.context);

  // Step 2: Generate prompts
  const generation = await generatePrompts(analysis, request.platforms);

  // Step 3: Build the response
  const processingTime = Date.now() - startTime;

  // Transform prompts to cleaner format
  const prompts: Record<string, any> = {};
  for (const [platformId, prompt] of Object.entries(generation.prompts)) {
    prompts[platformId] = {
      prompt: prompt.prompt,
      placeholders: prompt.placeholders.map((p) => ({
        key: p.key,
        description: p.description,
      })),
      settings: prompt.settings,
    };
  }

  // Build placeholders summary
  const placeholders = analysis.placeholders.map((p) => ({
    name: p.name,
    description: p.description,
    required: p.required,
  }));

  // Build assumptions (optionally filtered)
  const assumptions = request.options?.include_assumptions !== false
    ? analysis.assumptions.map((a) => ({
        category: a.category,
        value: a.value,
        reasoning: a.reasoning,
      }))
    : [];

  return {
    id: requestId,
    input: request.input,
    analysis: {
      intent: analysis.intent.primary,
      confidence: analysis.intent.confidence,
      entities: analysis.entities.map((e) => ({
        type: e.type,
        value: e.value,
      })),
    },
    prompts,
    placeholders,
    assumptions,
    metadata: {
      processing_time_ms: processingTime,
      platforms_generated: Object.keys(generation.prompts),
      timestamp: new Date().toISOString(),
    },
  };
}