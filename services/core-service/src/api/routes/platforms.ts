import { Router, Request, Response } from 'express';
import { getPlatforms, getIntents } from '../../services/generationClient';

const router = Router();

/**
 * GET /api/v1/platforms
 * 
 * List all available AI platforms.
 */
router.get('/platforms', async (req: Request, res: Response) => {
  try {
    const platforms = await getPlatforms();
    return res.json({ platforms });
  } catch (error: any) {
    console.error('Platforms error:', error.message);
    return res.status(500).json({
      error: 'Internal Server Error',
      message: 'Failed to fetch platforms',
    });
  }
});

/**
 * GET /api/v1/intents
 * 
 * List all supported intents.
 */
router.get('/intents', async (req: Request, res: Response) => {
  try {
    const intents = await getIntents();
    return res.json({ intents });
  } catch (error: any) {
    console.error('Intents error:', error.message);
    return res.status(500).json({
      error: 'Internal Server Error',
      message: 'Failed to fetch intents',
    });
  }
});

export default router;