import { Router, Request, Response } from 'express';
import { checkAnalysisHealth } from '../../services/analysisClient';
import { checkGenerationHealth } from '../../services/generationClient';
import { config } from '../../config';

const router = Router();

/**
 * GET /health
 * 
 * Basic health check.
 */
router.get('/health', (req: Request, res: Response) => {
  return res.json({
    status: 'healthy',
    service: config.serviceName,
  });
});

/**
 * GET /ready
 * 
 * Readiness check - verifies all dependencies are available.
 */
router.get('/ready', async (req: Request, res: Response) => {
  const analysisOk = await checkAnalysisHealth();
  const generationOk = await checkGenerationHealth();

  const ready = analysisOk && generationOk;

  return res.status(ready ? 200 : 503).json({
    ready,
    checks: {
      analysis_service: analysisOk,
      generation_service: generationOk,
    },
  });
});

export default router;