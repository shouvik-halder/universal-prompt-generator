import axios from 'axios';
import { config } from '../config';
import { AnalysisResponse, GenerationResponse } from '../models';

const client = axios.create({
  baseURL: config.generationServiceUrl,
  timeout: config.serviceTimeout,
  headers: {
    'Content-Type': 'application/json',
  },
});

export async function generatePrompts(
  analysis: AnalysisResponse,
  platforms?: string[]
): Promise<GenerationResponse> {
  const response = await client.post<GenerationResponse>('/generate', {
    analysis,
    platforms,
  });
  return response.data;
}

export async function getPlatforms(): Promise<any[]> {
  const response = await client.get('/platforms');
  return response.data;
}

export async function getIntents(): Promise<any[]> {
  const response = await client.get('/intents');
  return response.data;
}

export async function checkGenerationHealth(): Promise<boolean> {
  try {
    const response = await client.get('/health');
    return response.data.status === 'healthy';
  } catch {
    return false;
  }
}