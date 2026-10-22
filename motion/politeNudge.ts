/** Polite Nudge: deterministic cursor-contact displacement for visual ORBs.
 * Reference: POPS WebsiteFloatingOrb.tsx proximity repulsion.
 * The host Motion Runtime owns animation, movement authorization, docking and bounds.
 * No timers, browser APIs, LLM calls, or autonomous-roaming decisions occur here.
 */
export type Point = { x: number; y: number };
export type PoliteNudgeInput = {
  orbTopLeft: Point;
  cursor: Point;
  orbSize: number;
  viewport: { width: number; height: number };
  minY?: number;
  margin?: number;
  radiusScale?: number;
  maxStep?: number;
};
export type PoliteNudgeResult = { destination: Point; distance: number; strength: number } | null;
const clamp = (value: number, low: number, high: number) => Math.min(Math.max(value, low), Math.max(low, high));

export function calculatePoliteNudge(input: PoliteNudgeInput): PoliteNudgeResult {
  const { orbTopLeft, cursor, orbSize, viewport } = input;
  if (![orbTopLeft.x, orbTopLeft.y, cursor.x, cursor.y, orbSize, viewport.width, viewport.height].every(Number.isFinite) || orbSize <= 0) return null;
  const radius = orbSize * (input.radiusScale ?? 1.35);
  const dx = orbTopLeft.x + orbSize / 2 - cursor.x;
  const dy = orbTopLeft.y + orbSize / 2 - cursor.y;
  const distance = Math.hypot(dx, dy);
  if (distance >= radius) return null;
  // POPS proximity curve; clamp maximum per pointer movement to avoid sudden fleeing.
  const strength = (radius - distance) / radius;
  const step = strength * (input.maxStep ?? Math.min(24, orbSize * 0.16));
  if (step <= 0) return null;
  const length = Math.max(distance, 1);
  const margin = input.margin ?? 18;
  const destination = {
    x: clamp(orbTopLeft.x + (distance > 0.01 ? dx / length : 1) * step, margin, viewport.width - orbSize - margin),
    y: clamp(orbTopLeft.y + (distance > 0.01 ? dy / length : 0) * step, input.minY ?? 92, viewport.height - orbSize - margin),
  };
  if (Math.hypot(destination.x - orbTopLeft.x, destination.y - orbTopLeft.y) < 0.5) return null;
  return { destination, distance, strength };
}
