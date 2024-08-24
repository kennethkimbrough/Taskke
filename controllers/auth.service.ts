// services/auth.service.ts
import { Injectable } from '@nestjs/common';
import { UserService } from './user.service';
import * as bcrypt from 'bcrypt';
import * as jwt from 'jsonwebtoken';

@Injectable()
export class AuthService {
  constructor(private readonly userService: UserService) {}

  async register(user: { name: string; email: string; password: string }) {
    const existingUser = await this.userService.findOne({ email: user.email });
    if (existingUser) {
      throw new Error('User already exists');
    }
    const newUser = await this.userService.create(user);
    return this.generateToken(newUser);
  }

  async login(email: string, password: string) {
    const user = await this.userService.findOne({ email });
    if (!user) {
      throw new Error('Invalid email or password');
    }
    const isValid = await bcrypt.compare(password, user.password);
    if (!isValid) {
      throw new Error('Invalid email or password');
    }
    return this.generateToken(user);
  }

  private generateToken(user: User) {
    const token = jwt.sign({ userId: user.id, email: user.email }, process.env.SECRET_KEY, {
      expiresIn: '1h',
    });
    return token;
  }
}
