import Nav from './components/Nav';
import HeroContent from './components/HeroContent';

const VIDEO_SRC =
  'https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260721_194026_53c6f9fd-f0d7-4d7d-be62-cdd53b253fb3.mp4';

export default function App() {
  return (
    <div className="relative" style={{ backgroundColor: '#0A061A' }}>
      <div className="relative z-0">
        <div className="sticky top-0 h-screen w-full overflow-hidden">
          <video
            autoPlay
            muted
            loop
            playsInline
            className="w-full h-full object-cover"
            src={VIDEO_SRC}
          />
          <div
            className="absolute inset-x-0 bottom-0 h-[40%] pointer-events-none"
            style={{ background: 'linear-gradient(to bottom, transparent, #0A061A)' }}
          />
        </div>

        <div className="relative z-10 -mt-[100vh]">
          <Nav />
          <HeroContent />
        </div>
      </div>
    </div>
  );
}
