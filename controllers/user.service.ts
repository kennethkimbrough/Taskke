// services/user.service.ts
import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { User } from '../entities/User';
import { AuthService } from './auth.service';

@Injectable()
export class UserService {
  constructor(
    @InjectRepository(User)
    private readonly userRepository: Repository<User>,
    private readonly authService: AuthService,
  ) {}

  async findOne(options: any) {
    return this.userRepository.findOne(options);
  }

  async create(user: { name: string; email: string; password: string }) {
    return this.userRepository.save(user);
  }

  async register(user: { name: string; email: string; password: string }) {
    return this.authService.register(user);
  }

  async login(email: string, password: string) {
    return this.authService.login(email, password);
  }
}
