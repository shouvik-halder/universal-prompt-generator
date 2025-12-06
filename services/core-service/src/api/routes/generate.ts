import { Router, Request, Response } from 'express';
import { orchestrate } from '../../core/orchestrator';
import { GenerateRequest } from '../../models';

const router = Router();

/**
 * POST /api/v1/generate
 * 
 * Main endpoint to generate AI prompts from user input.
 */
router.post('/', async (req: Request, res: Response) => {
  try {
    const { input, context, platforms, options } = req.body as GenerateRequest;

    // Validate input
    if (!input || typeof input !== 'string' || input.trim().length === 0) {
      return res.status(400).json({
        error: 'Bad Request',
        message: 'Input text is required',
      });
    }

    if (input.length > 10000) {
      return res.status(400).json({
        error: 'Bad Request',
        message: 'Input text exceeds maximum length of 10000 characters',
      });
    }

    // Run orchestration pipeline
    const result = await orchestrate({
      input: input.trim(),
      context,
      platforms,
      options,
    });

    return res.json(result);
  } catch (error: any) {
    console.error('Generate error:', error.message);
    
    // Check if it's a service error
    if (error.response) {
      return res.status(502).json({
        error: 'Service Error',
        message: 'Failed to communicate with backend services',
        details: error.response.data,
      });
    }

    return res.status(500).json({
      error: 'Internal Server Error',
      message: error.message || 'An unexpected error occurred',
    });
  }
});

export default router;