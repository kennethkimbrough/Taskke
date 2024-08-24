import { resolve } from 'path';

const dbHost = process.env.DB_HOST;
const dbPort = process.env.DB_PORT;
const dbUsername = process.env.DB_USERNAME;
const dbPassword = process.env.DB_PASSWORD;
const dbName = process.env.DB_NAME;

module.exports = {
  type: 'postgres',
  url: `postgres://${dbUsername}:${dbPassword}@${dbHost}:${dbPort}/${dbName}`,
  entities: [resolve(__dirname, './**/*.entity{.ts,.js}')],
  migrations: [resolve(__dirname, './migrations/**/*{.ts,.js}')],
  cli: {
    migrationsDir: 'src/migrations',
  },
};
