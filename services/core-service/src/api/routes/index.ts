import { Router } from 'express';
import generateRouter from './generate';
import platformsRouter from './platforms';
import healthRouter from './health';

const router = Router();

// Health routes (no prefix)
router.use('/', healthRouter);

// API v1 routes
router.use('/api/v1/generate', generateRouter);
router.use('/api/v1', platformsRouter);

export default router;