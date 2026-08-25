const AVATARS = [
  'https://images.pexels.com/photos/2379004/pexels-photo-2379004.jpeg?auto=compress&cs=tinysrgb&w=100',
  'https://images.pexels.com/photos/1239291/pexels-photo-1239291.jpeg?auto=compress&cs=tinysrgb&w=100',
  'https://images.pexels.com/photos/1681010/pexels-photo-1681010.jpeg?auto=compress&cs=tinysrgb&w=100',
  'https://images.pexels.com/photos/774909/pexels-photo-774909.jpeg?auto=compress&cs=tinysrgb&w=100',
];

export default function HeroContent() {
  return (
    <section className="px-6 sm:px-8 md:px-12 pt-24 md:pt-32 pb-20 md:pb-40">
      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-12 items-start">
        <div>
          <h1 className="text-white text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-light leading-[1.1] tracking-tight">
            Outsourced
            <br />
            development
            <br />
            team
          </h1>
          <p className="text-white/50 text-sm mt-6 font-light">
            Built off-site. Feels in-house.
          </p>
        </div>

        <div className="flex flex-col items-start md:items-end gap-4">
          <div className="flex -space-x-2 mb-2">
            {AVATARS.map((src) => (
              <img
                key={src}
                src={src}
                alt=""
                className="w-8 h-8 rounded-full border-2 border-black/50 object-cover"
              />
            ))}
          </div>

          <div className="max-w-sm w-full rounded-2xl liquid-glass p-5">
            <p className="text-white/90 text-sm font-light leading-relaxed">
              Working with this team felt like unlocking a cheat code. I sent them a Figma + a
              wild idea, and a week later I had a working prototype with pixel-perfect
              animations. Fully remote, yet fully in sync.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
