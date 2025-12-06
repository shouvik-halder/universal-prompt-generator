import app from './app';
import { config } from './config';

const PORT = config.port;

app.listen(PORT, () => {
  console.log(`🚀 ${config.serviceName} running on port ${PORT}`);
  console.log(`   Analysis service: ${config.analysisServiceUrl}`);
  console.log(`   Generation service: ${config.generationServiceUrl}`);
});