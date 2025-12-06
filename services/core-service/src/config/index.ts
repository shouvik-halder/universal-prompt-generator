export const config = {
  serviceName: process.env.SERVICE_NAME || 'core-service',
  port: parseInt(process.env.PORT || '8000', 10),
  
  // Service URLs
  analysisServiceUrl: process.env.ANALYSIS_SERVICE_URL || 'http://localhost:8001',
  generationServiceUrl: process.env.GENERATION_SERVICE_URL || 'http://localhost:8002',
  
  // Timeouts
  serviceTimeout: parseInt(process.env.SERVICE_TIMEOUT || '10000', 10),
};