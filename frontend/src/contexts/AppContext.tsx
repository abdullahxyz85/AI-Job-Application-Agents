import React, { createContext, useContext, useState, ReactNode } from 'react';

interface User {
  id: string;
  name: string;
  email: string;
  avatar?: string;
  level: number;
  badges: string[];
  applicationsSubmitted: number;
}

interface Job {
  id: string;
  title: string;
  company: string;
  logo: string;
  location: string;
  description: string;
  matchScore: number;
  applied: boolean;
  salary?: string;
  type: 'Full-time' | 'Part-time' | 'Contract';
}

interface AuditLogEntry {
  id: string;
  timestamp: Date;
  agent: 'resume-parser' | 'job-searcher' | 'cover-letter-generator' | 'auditor';
  action: string;
  details: string;
  status: 'success' | 'pending' | 'error';
}

interface AppContextType {
  user: User | null;
  jobs: Job[];
  auditLog: AuditLogEntry[];
  resumeUploaded: boolean;
  setResumeUploaded: (uploaded: boolean) => void;
  addAuditEntry: (entry: Omit<AuditLogEntry, 'id' | 'timestamp'>) => void;
  applyToJob: (jobId: string) => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export const AppProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User>({
    id: '1',
    name: 'Alex Johnson',
    email: 'alex@example.com',
    level: 3,
    badges: ['Quick Starter', 'Profile Complete', 'First Application'],
    applicationsSubmitted: 12
  });

  const [resumeUploaded, setResumeUploaded] = useState(false);

  const [jobs] = useState<Job[]>([
    {
      id: '1',
      title: 'Senior Frontend Developer',
      company: 'TechCorp',
      logo: '🏢',
      location: 'San Francisco, CA',
      description: 'Build amazing user experiences with React and TypeScript',
      matchScore: 95,
      applied: false,
      salary: '$120k - $160k',
      type: 'Full-time'
    },
    {
      id: '2',
      title: 'Full Stack Engineer',
      company: 'StartupInc',
      logo: '🚀',
      location: 'Remote',
      description: 'Join our growing team to build the next big thing',
      matchScore: 88,
      applied: true,
      salary: '$100k - $140k',
      type: 'Full-time'
    },
    {
      id: '3',
      title: 'UI/UX Designer',
      company: 'DesignStudio',
      logo: '🎨',
      location: 'New York, NY',
      description: 'Create beautiful and intuitive user interfaces',
      matchScore: 72,
      applied: false,
      salary: '$90k - $120k',
      type: 'Full-time'
    }
  ]);

  const [auditLog, setAuditLog] = useState<AuditLogEntry[]>([
    {
      id: '1',
      timestamp: new Date(Date.now() - 1000 * 60 * 30),
      agent: 'resume-parser',
      action: 'Resume Parsed',
      details: 'Extracted skills: React, TypeScript, Node.js',
      status: 'success'
    },
    {
      id: '2',
      timestamp: new Date(Date.now() - 1000 * 60 * 25),
      agent: 'job-searcher',
      action: 'Job Search',
      details: 'Found 25 matching positions',
      status: 'success'
    },
    {
      id: '3',
      timestamp: new Date(Date.now() - 1000 * 60 * 20),
      agent: 'cover-letter-generator',
      action: 'Cover Letter Generated',
      details: 'Created personalized cover letter for TechCorp',
      status: 'success'
    }
  ]);

  const addAuditEntry = (entry: Omit<AuditLogEntry, 'id' | 'timestamp'>) => {
    const newEntry: AuditLogEntry = {
      ...entry,
      id: Math.random().toString(36).substr(2, 9),
      timestamp: new Date()
    };
    setAuditLog(prev => [newEntry, ...prev]);
  };

  const applyToJob = (jobId: string) => {
    // Update job application status and add audit entry
    addAuditEntry({
      agent: 'auditor',
      action: 'Application Submitted',
      details: `Applied to ${jobs.find(j => j.id === jobId)?.title}`,
      status: 'success'
    });
  };

  return (
    <AppContext.Provider value={{
      user,
      jobs,
      auditLog,
      resumeUploaded,
      setResumeUploaded,
      addAuditEntry,
      applyToJob
    }}>
      {children}
    </AppContext.Provider>
  );
};

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within AppProvider');
  }
  return context;
};