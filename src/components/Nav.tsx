import { useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { Menu, X } from 'lucide-react';

const LINKS = ['About', 'Our cases', 'Services', 'Prices'];
const ACTIVE = 'About';

export default function Nav() {
  const [open, setOpen] = useState(false);

  return (
    <>
      <nav className="fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-6 sm:px-8 md:px-12 py-5 md:py-6">
        <a href="#" className="text-white font-light text-lg tracking-wide">
          DE&lt;/<span className="font-normal">HELPERS</span>
        </a>

        <div className="hidden md:flex items-center gap-2">
          {LINKS.map((link) => (
            <a
              key={link}
              href="#"
              className={`text-sm px-4 py-2 rounded-full transition-all duration-300 ${
                link === ACTIVE
                  ? 'border border-white/60 text-white'
                  : 'text-white/70 hover:text-white'
              }`}
            >
              {link}
            </a>
          ))}
          <button className="bg-white text-black text-sm font-medium px-5 py-2 rounded-full hover:bg-white/90 ml-4 transition-all duration-300">
            Hire us
          </button>
        </div>

        <button
          type="button"
          aria-label={open ? 'Close menu' : 'Open menu'}
          onClick={() => setOpen((v) => !v)}
          className="md:hidden relative z-[60] w-10 h-10 flex items-center justify-center text-white"
        >
          <AnimatePresence mode="wait">
            {open ? (
              <motion.span
                key="close"
                initial={{ opacity: 0, rotate: -90 }}
                animate={{ opacity: 1, rotate: 0 }}
                exit={{ opacity: 0, rotate: 90 }}
                transition={{ duration: 0.2 }}
                className="flex"
              >
                <X size={24} />
              </motion.span>
            ) : (
              <motion.span
                key="menu"
                initial={{ opacity: 0, rotate: 90 }}
                animate={{ opacity: 1, rotate: 0 }}
                exit={{ opacity: 0, rotate: -90 }}
                transition={{ duration: 0.2 }}
                className="flex"
              >
                <Menu size={24} />
              </motion.span>
            )}
          </AnimatePresence>
        </button>
      </nav>

      <AnimatePresence>
        {open && (
          <div className="fixed inset-0 z-[55] md:hidden">
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.3 }}
              className="absolute inset-0 bg-black/95 backdrop-blur-xl"
            />

            <motion.button
              type="button"
              aria-label="Close menu"
              onClick={() => setOpen(false)}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2 }}
              className="absolute top-5 right-6 sm:right-8 w-10 h-10 flex items-center justify-center text-white"
            >
              <X size={24} />
            </motion.button>

            <div className="relative h-full flex flex-col items-center justify-center gap-8">
              {LINKS.map((link, i) => (
                <motion.a
                  key={link}
                  href="#"
                  onClick={() => setOpen(false)}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 20 }}
                  transition={{ delay: 0.15 + i * 0.05, duration: 0.3 }}
                  className={`text-2xl font-light ${
                    link === ACTIVE ? 'text-white' : 'text-white/70 hover:text-white'
                  } transition-all duration-300`}
                >
                  {link}
                </motion.a>
              ))}

              <motion.button
                type="button"
                onClick={() => setOpen(false)}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 20 }}
                transition={{ delay: 0.4, duration: 0.3 }}
                className="bg-white text-black text-lg font-medium px-8 py-3 rounded-full hover:bg-white/90 transition-all duration-300"
              >
                Hire us
              </motion.button>
            </div>
          </div>
        )}
      </AnimatePresence>
    </>
  );
}
