import { memo } from 'react';

const particles = Array.from({ length: 46 }, (_, index) => ({
  id: index,
  left: `${(index * 37) % 100}%`,
  top: `${(index * 61) % 100}%`,
  delay: `${(index % 11) * 0.7}s`,
  duration: `${8 + (index % 7)}s`,
  size: `${2 + (index % 3)}px`
}));

function ParticleField() {
  return (
    <div className="particle-field" aria-hidden="true">
      <div className="scan-grid" />
      {particles.map((particle) => (
        <span
          key={particle.id}
          className="particle-dot"
          style={{
            left: particle.left,
            top: particle.top,
            width: particle.size,
            height: particle.size,
            animationDelay: particle.delay,
            animationDuration: particle.duration
          }}
        />
      ))}
    </div>
  );
}

export default memo(ParticleField);
