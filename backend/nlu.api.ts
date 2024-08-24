// rasa_nlu_api.ts
import { Controller, Post, Body, Req, Res } from '@nestjs/common';
import { AuthService } from './auth.service';
import { UserService } from './user.service';

@Controller('chat')
export class RasaNLUAPI {
  constructor(private readonly authService: AuthService, private readonly userService: UserService) {}

  @Post()
  async handleChat(@Body() message: string, @Req() req: Request, @Res() res: Response) {
    const token = req.headers['authorization'];
    if (!token) {
      return res.status(401).json({ error: 'Unauthorized' });
    }
    const user = await this.authService.verifyToken(token);
    if (!user) {
      return res.status(401).json({ error: 'Unauthorized' });
    }
    // Process chat message
  }
}
