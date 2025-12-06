import axios from 'axios';
import { config } from '../config';
import { AnalysisResponse } from '../models';

const client = axios.create({
  baseURL: config.analysisServiceUrl,
  timeout: config.serviceTimeout,
  headers: {
    'Content-Type': 'application/json',
  },
});

export async function analyzeText(
  text: string,
  context?: string
): Promise<AnalysisResponse> {
  const response = await client.post<AnalysisResponse>('/analyze', {
    text,
    context,
  });
  return response.data;
}

export async function checkAnalysisHealth(): Promise<boolean> {
  try {
    const response = await client.get('/health');
    return response.data.status === 'healthy';
  } catch {
    return false;
  }
}