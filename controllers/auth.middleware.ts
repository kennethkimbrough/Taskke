// auth.middleware.ts
import { Injectable } from '@nestjs/common';
import { AuthService } from './auth.service';

@Injectable()
export class AuthMiddleware {
  constructor(private readonly authService: AuthService) {}

  async use(req: Request, res: Response, next: () => void)
