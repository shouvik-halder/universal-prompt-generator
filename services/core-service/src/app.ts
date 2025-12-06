import express from 'express';
import cors from 'cors';
import routes from './api/routes';
import { config } from './config';

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Request logging
app.use((req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    const duration = Date.now() - start;
    console.log(`${req.method} ${req.path} ${res.statusCode} ${duration}ms`);
  });
  next();
});

// Routes
app.use(routes);

// Root endpoint
app.get('/', (req, res) => {
  res.json({
    service: config.serviceName,
    version: '1.0.0',
    status: 'running',
    endpoints: {
      generate: 'POST /api/v1/generate',
      platforms: 'GET /api/v1/platforms',
      intents: 'GET /api/v1/intents',
      health: 'GET /health',
      ready: 'GET /ready',
    },
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    error: 'Not Found',
    message: `Route ${req.method} ${req.path} not found`,
  });
});

// Error handler
app.use((err: Error, req: express.Request, res: express.Response, next: express.NextFunction) => {
  console.error('Unhandled error:', err);
  res.status(500).json({
    error: 'Internal Server Error',
    message: err.message,
  });
});

export default app;