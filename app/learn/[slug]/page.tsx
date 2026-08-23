import { notFound } from 'next/navigation';
import type { Metadata } from 'next';
import lessonsData from '../../data/lessons.json';
import type { Lesson } from '../../data/types';
import LessonClient from './LessonClient';

const lessons = lessonsData as Lesson[];

export function generateStaticParams() {
  return lessons.map((lesson) => ({ slug: lesson.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const lesson = lessons.find((item) => item.slug === slug);
  if (!lesson) return {};
  return {
    title: `${lesson.title} — PyReady`,
    description: lesson.summary,
    openGraph: { title: `${lesson.title} — PyReady`, description: lesson.summary, images: [] },
    twitter: { card: 'summary', title: `${lesson.title} — PyReady`, description: lesson.summary, images: [] },
  };
}

export default async function LessonPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const lesson = lessons.find((item) => item.slug === slug);
  if (!lesson) notFound();
  return <LessonClient lesson={lesson} lessons={lessons} />;
}
