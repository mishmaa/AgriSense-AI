import { motion, useReducedMotion } from 'framer-motion';
import { cn } from '../../utils/formatters.js';

export default function GlassPanel({ children, className, delay = 0, as = motion.div }) {
  const Component = as;
  const reduceMotion = useReducedMotion();

  return (
    <Component
      initial={reduceMotion ? false : { opacity: 0, y: 18, rotateX: 2 }}
      whileInView={reduceMotion ? undefined : { opacity: 1, y: 0, rotateX: 0 }}
      viewport={{ once: true, margin: '-60px' }}
      whileHover={reduceMotion ? undefined : { y: -4, rotateX: 0.8, rotateY: -0.8 }}
      transition={{ duration: 0.5, delay, ease: [0.16, 1, 0.3, 1] }}
      className={cn('glass premium-surface relative rounded-lg', className)}
    >
      {children}
    </Component>
  );
}
