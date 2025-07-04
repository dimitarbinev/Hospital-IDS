"use client";

import Link from "next/link";
import { ShieldCheck, Activity, Server, Clock } from "lucide-react";

export default function HomePage() {
  return (
    <main className="min-h-screen flex flex-col bg-gradient-to-br from-slate-50 to-white text-slate-800">
      <header className="fixed inset-x-0 top-0 z-50 bg-white/70 backdrop-blur-lg">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <Link href="/" className="text-lg font-bold tracking-tight">
            Hospital IDS
          </Link>
          <nav className="hidden gap-8 text-sm font-medium sm:flex">
            <Link href="#features" className="transition hover:text-blue-600">
              Features
            </Link>
            <Link href="#about" className="transition hover:text-blue-600">
              About
            </Link>
            <Link href="#contact" className="transition hover:text-blue-600">
              Contact
            </Link>
          </nav>
        </div>
      </header>

      <section className="flex grow items-center pt-24">
        <div className="mx-auto w-full max-w-3xl px-6 text-center">
          <h1 className="text-4xl font-extrabold leading-tight tracking-tight sm:text-6xl">
            Hospital IoT Intrusion Detection
          </h1>
          <p className="mt-6 text-lg text-slate-600 sm:text-xl">
            Real‑time threat monitoring and rapid response powered by RTC
            back‑end architecture, safeguarding critical medical devices around
            the clock.
          </p>
          <div className="mt-8 flex flex-wrap justify-center gap-4">
            <Link
              href="/dashboard"
              className="rounded-lg bg-blue-600 px-6 py-3 text-white transition hover:bg-blue-700"
            >
              Launch Dashboard
            </Link>
            <Link
              href="#features"
              className="rounded-lg bg-slate-200 px-6 py-3 text-slate-800 transition hover:bg-slate-300"
            >
              Learn More
            </Link>
          </div>
        </div>
      </section>

      <section id="features" className="bg-white py-24">
        <div className="mx-auto grid max-w-7xl grid-cols-1 gap-12 px-6 sm:grid-cols-2 lg:grid-cols-4">
          <div className="flex flex-col items-center text-center">
            <ShieldCheck className="h-12 w-12 text-blue-600" />
            <h3 className="mt-4 text-xl font-semibold">Real‑Time Detection</h3>
            <p className="mt-2 text-sm text-slate-500">
              Instant alerts for anomalous traffic and device behaviour.
            </p>
          </div>
          <div className="flex flex-col items-center text-center">
            <Activity className="h-12 w-12 text-blue-600" />
            <h3 className="mt-4 text-xl font-semibold">Predictive Analytics</h3>
            <p className="mt-2 text-sm text-slate-500">
              Machine‑learning models anticipate threats before they escalate.
            </p>
          </div>
          <div className="flex flex-col items-center text-center">
            <Server className="h-12 w-12 text-blue-600" />
            <h3 className="mt-4 text-xl font-semibold">Scalable RTC Core</h3>
            <p className="mt-2 text-sm text-slate-500">
              Low‑latency back‑end streams telemetry over secure WebRTC
              channels.
            </p>
          </div>
          <div className="flex flex-col items-center text-center">
            <Clock className="h-12 w-12 text-blue-600" />
            <h3 className="mt-4 text-xl font-semibold">24/7 Monitoring</h3>
            <p className="mt-2 text-sm text-slate-500">
              Continuous protection with automated remediation workflows.
            </p>
          </div>
        </div>
      </section>

      <section id="about" className="bg-slate-50 py-24">
        <div className="mx-auto max-w-3xl px-6 text-center">
          <h2 className="text-3xl font-bold tracking-tight">
            Built for Modern Hospitals
          </h2>
          <p className="mt-4 text-lg text-slate-600">
            The system seamlessly integrates with existing hospital networks,
            providing actionable insights and a unified dashboard to ensure
            compliance, patient safety, and operational continuity. Powered by a
            resilient RTC back‑end, data flows securely and efficiently even
            under peak load.
          </p>
        </div>
      </section>

      <section id="contact" className="bg-white py-24">
        <div className="mx-auto max-w-xl px-6 text-center">
          <h2 className="text-3xl font-bold tracking-tight">Get in Touch</h2>
          <p className="mt-4 text-lg text-slate-600">
            Reach out to discuss deployment, partnership opportunities, or
            custom integrations.
          </p>
          <Link
            href="mailto:info@hospitalids.io"
            className="mt-8 inline-block rounded-lg bg-blue-600 px-8 py-3 text-white transition hover:bg-blue-700"
          >
            Contact Us
          </Link>
        </div>
      </section>

      <footer className="bg-slate-900 py-8 text-center text-sm text-slate-400">
        <p>© {new Date().getFullYear()} Hospital IDS. All rights reserved.</p>
      </footer>
    </main>
  );
}
