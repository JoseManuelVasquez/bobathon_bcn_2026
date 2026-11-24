// Keep previous workshop notes and bookmarks useful when steps become milestones.
// A milestone is complete only when every former required step was complete.
export function migrateProgress(record, courses) {
  if (record.guideVersion >= 2) return record;
  const completed = { ...record.completed };
  const notes = { ...record.notes };
  for (const course of courses) {
    for (const section of course.sections) {
      const target = `${course.id}/${section.id}`;
      const sources = section.sourceIds || [];
      completed[target] = sources.length > 0 && sources.every(id => record.completed?.[`${course.id}/${id}`] === true);
      const noteIds = [...new Set([...sources, ...(section.noteIds || [])])];
      const entries = noteIds.map(id => ({ id, text: record.notes?.[`${course.id}/${id}`] }))
        .filter(entry => typeof entry.text === 'string' && entry.text.trim());
      if (entries.length) {
        notes[target] = entries.length === 1 && entries[0].id === section.id
          ? entries[0].text
          : entries.map(({ id, text }) => `${section.legacyTitles?.[id] || id}:\n${text}`).join('\n\n');
      }
    }
  }
  return { ...record, completed, notes, guideVersion: 2 };
}
