import type { VercelRequest, VercelResponse } from '@vercel/node';
import crypto from 'crypto';

export default function handler(req: VercelRequest, res: VercelResponse) {
  const signature = crypto.createHmac('sha256', process.env.SECRET || '').update(JSON.stringify(req.body)).digest('hex');
  res.status(200).json({ sovereign: true, resonance: "full", signature });
}
