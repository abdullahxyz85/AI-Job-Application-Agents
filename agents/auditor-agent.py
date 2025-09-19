#!/usr/bin/env python3
"""
🔍 CORAL PROTOCOL AGENT: Auditor
===============================
Hackathon Project: AI Job Application Agent
Agent: Auditor - Logs all actions and provides transparency
Author: Hackathon Team
Version: 1.0

This agent provides transparency and accountability by:
- Logging all agent activities and decisions
- Tracking application workflow progress
- Providing audit trails for compliance
- Monitoring agent performance and errors
- Generating reports and analytics
"""

import sys
import time
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import sqlite3
import os

class AuditorAgent:
    """
    🔍 Auditor Agent for AI Job Application System
    
    Responsibilities:
    - Log all agent activities and decisions
    - Track application workflow progress  
    - Provide transparency and audit trails
    - Monitor system performance
    - Generate compliance reports
    - Detect and alert on anomalies
    """
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.coral_server = "http://localhost:5555"
        self.agent_id = None
        self.thread_id = None
        
        # Initialize audit database
        self.db_path = "audit_log.db"
        self.init_database()
        
        # Audit categories
        self.audit_categories = {
            "resume_processing": "Resume Parser Activities",
            "job_search": "Job Search Activities", 
            "cover_letter": "Cover Letter Generation",
            "application": "Job Application Process",
            "system": "System and Infrastructure",
            "compliance": "Compliance and Security",
            "performance": "Performance Metrics"
        }
        
        # Connect to Coral server
        self.connect_to_coral_server()
        
    def connect_to_coral_server(self):
        """Connect and register with coral-server"""
        try:
            # Test connection
            response = requests.get(f"{self.coral_server}/api/v1/agents")
            if response.status_code != 200:
                raise Exception(f"Cannot connect to coral-server at {self.coral_server}")
                
            print("✅ Connected to coral-server at", self.coral_server)
            
            # Register agent
            self.register_agent()
            self.create_thread()
            
        except Exception as e:
            print(f"❌ Failed to connect to coral-server: {e}")
            sys.exit(1)
    
    def register_agent(self):
        """Register this agent with coral-server"""
        try:
            print(f"🤖 Registering Auditor Agent: {self.agent_name}")
            
            agent_data = {
                "name": self.agent_name,
                "type": "auditor",
                "version": "1.0",
                "description": "Provides audit trails and transparency for all agent activities",
                "capabilities": [
                    "activity_logging",
                    "audit_trail_generation",
                    "compliance_monitoring", 
                    "performance_tracking",
                    "anomaly_detection",
                    "reporting_analytics"
                ]
            }
            
            # Note: coral-server auto-registers agents, so we just confirm registration
            print(f"✅ Agent '{self.agent_name}' registered successfully")
            
        except Exception as e:
            print(f"❌ Failed to register agent: {e}")
            sys.exit(1)
    
    def create_thread(self):
        """Create communication thread"""
        try:
            # Generate unique thread ID
            self.thread_id = f"thread_{hash(self.agent_name) % 10000000}"
            print(f"🧵 Created communication thread: {self.thread_id}")
            
        except Exception as e:
            print(f"❌ Failed to create thread: {e}")
            sys.exit(1)
    
    def init_database(self):
        """Initialize SQLite database for audit logs"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create audit_logs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    agent_name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    action TEXT NOT NULL,
                    details TEXT,
                    status TEXT NOT NULL,
                    duration_ms INTEGER,
                    metadata TEXT
                )
            ''')
            
            # Create performance_metrics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    metric_name TEXT NOT NULL,
                    metric_value REAL NOT NULL,
                    agent_name TEXT,
                    metadata TEXT
                )
            ''')
            
            # Create application_workflow table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS application_workflow (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    application_id TEXT NOT NULL,
                    candidate_name TEXT,
                    job_title TEXT,
                    company_name TEXT,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    workflow_data TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
            
            print(f"📊 Initialized audit database: {self.db_path}")
            
        except Exception as e:
            print(f"❌ Failed to initialize database: {e}")
            sys.exit(1)
    
    def log_activity(self, agent_name: str, category: str, action: str, 
                    details: str = "", status: str = "success", 
                    duration_ms: int = 0, metadata: Dict = None):
        """Log an agent activity to the audit database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO audit_logs 
                (timestamp, agent_name, category, action, details, status, duration_ms, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                agent_name,
                category,
                action,
                details,
                status,
                duration_ms,
                json.dumps(metadata) if metadata else None
            ))
            
            conn.commit()
            conn.close()
            
            # Display log entry
            status_icon = "✅" if status == "success" else "❌" if status == "error" else "⏳"
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {status_icon} {agent_name}: {action}")
            if details:
                print(f"    📝 {details}")
            
        except Exception as e:
            print(f"❌ Failed to log activity: {e}")
    
    def track_application_workflow(self, application_id: str, candidate_name: str, 
                                 job_title: str, company_name: str, status: str,
                                 workflow_data: Dict = None):
        """Track application workflow progress"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if application already exists
            cursor.execute('''
                SELECT id FROM application_workflow WHERE application_id = ?
            ''', (application_id,))
            
            existing = cursor.fetchone()
            
            if existing:
                # Update existing application
                cursor.execute('''
                    UPDATE application_workflow 
                    SET status = ?, updated_at = ?, workflow_data = ?
                    WHERE application_id = ?
                ''', (
                    status,
                    datetime.now().isoformat(),
                    json.dumps(workflow_data) if workflow_data else None,
                    application_id
                ))
            else:
                # Create new application record
                cursor.execute('''
                    INSERT INTO application_workflow 
                    (application_id, candidate_name, job_title, company_name, 
                     status, created_at, updated_at, workflow_data)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    application_id,
                    candidate_name,
                    job_title,
                    company_name,
                    status,
                    datetime.now().isoformat(),
                    datetime.now().isoformat(),
                    json.dumps(workflow_data) if workflow_data else None
                ))
            
            conn.commit()
            conn.close()
            
            print(f"📋 Application {application_id}: {status}")
            print(f"    👤 Candidate: {candidate_name}")
            print(f"    🎯 Position: {job_title} at {company_name}")
            
        except Exception as e:
            print(f"❌ Failed to track application workflow: {e}")
    
    def record_performance_metric(self, metric_name: str, metric_value: float, 
                                agent_name: str = None, metadata: Dict = None):
        """Record a performance metric"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO performance_metrics 
                (timestamp, metric_name, metric_value, agent_name, metadata)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                metric_name,
                metric_value,
                agent_name,
                json.dumps(metadata) if metadata else None
            ))
            
            conn.commit()
            conn.close()
            
            print(f"📊 Metric: {metric_name} = {metric_value}" + (f" ({agent_name})" if agent_name else ""))
            
        except Exception as e:
            print(f"❌ Failed to record performance metric: {e}")
    
    def generate_audit_report(self, hours: int = 24) -> Dict:
        """Generate audit report for the last N hours"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Calculate time range
            end_time = datetime.now()
            start_time = end_time - timedelta(hours=hours)
            
            # Get activity summary
            cursor.execute('''
                SELECT category, status, COUNT(*) as count
                FROM audit_logs 
                WHERE timestamp >= ? AND timestamp <= ?
                GROUP BY category, status
            ''', (start_time.isoformat(), end_time.isoformat()))
            
            activity_summary = {}
            for row in cursor.fetchall():
                category, status, count = row
                if category not in activity_summary:
                    activity_summary[category] = {}
                activity_summary[category][status] = count
            
            # Get performance metrics
            cursor.execute('''
                SELECT metric_name, AVG(metric_value) as avg_value, COUNT(*) as count
                FROM performance_metrics 
                WHERE timestamp >= ? AND timestamp <= ?
                GROUP BY metric_name
            ''', (start_time.isoformat(), end_time.isoformat()))
            
            performance_summary = {}
            for row in cursor.fetchall():
                metric_name, avg_value, count = row
                performance_summary[metric_name] = {
                    "average": round(avg_value, 2),
                    "count": count
                }
            
            # Get application workflow summary
            cursor.execute('''
                SELECT status, COUNT(*) as count
                FROM application_workflow 
                WHERE updated_at >= ? AND updated_at <= ?
                GROUP BY status
            ''', (start_time.isoformat(), end_time.isoformat()))
            
            workflow_summary = {}
            for row in cursor.fetchall():
                status, count = row
                workflow_summary[status] = count
            
            conn.close()
            
            report = {
                "report_generated": datetime.now().isoformat(),
                "time_range": {
                    "start": start_time.isoformat(),
                    "end": end_time.isoformat(),
                    "duration_hours": hours
                },
                "activity_summary": activity_summary,
                "performance_metrics": performance_summary,
                "application_workflow": workflow_summary
            }
            
            return report
            
        except Exception as e:
            print(f"❌ Failed to generate audit report: {e}")
            return {}
    
    def display_audit_report(self, report: Dict):
        """Display audit report in a formatted way"""
        print(f"\n📊 AUDIT REPORT")
        print("=" * 60)
        print(f"🕐 Time Range: {report['time_range']['duration_hours']} hours")
        print(f"📅 Generated: {report['report_generated'][:19]}")
        
        print(f"\n🔍 ACTIVITY SUMMARY:")
        for category, statuses in report['activity_summary'].items():
            total_activities = sum(statuses.values())
            print(f"   📋 {self.audit_categories.get(category, category)}: {total_activities} activities")
            for status, count in statuses.items():
                status_icon = "✅" if status == "success" else "❌" if status == "error" else "⏳"
                print(f"      {status_icon} {status}: {count}")
        
        if report['performance_metrics']:
            print(f"\n📊 PERFORMANCE METRICS:")
            for metric_name, data in report['performance_metrics'].items():
                print(f"   📈 {metric_name}: {data['average']} (avg of {data['count']} measurements)")
        
        if report['application_workflow']:
            print(f"\n📋 APPLICATION WORKFLOW:")
            total_applications = sum(report['application_workflow'].values())
            print(f"   📝 Total Applications: {total_applications}")
            for status, count in report['application_workflow'].items():
                print(f"      🎯 {status}: {count}")
    
    def simulate_audit_activities(self):
        """Simulate receiving and logging activities from other agents"""
        print(f"\n🎬 DEMO: Simulating Agent Activities to Audit")
        print("=" * 60)
        
        # Simulate resume parser activities
        self.log_activity(
            "resume-parser-agent", "resume_processing", "Resume Uploaded",
            "PDF resume successfully parsed, extracted 8 skills", "success", 1200
        )
        
        self.log_activity(
            "resume-parser-agent", "resume_processing", "Skills Extracted",
            "Identified: React, TypeScript, Node.js, Python, AWS, Docker, Git, SQL", "success", 800
        )
        
        time.sleep(1)
        
        # Simulate job searcher activities
        self.log_activity(
            "job-searcher-agent", "job_search", "Job Search Initiated",
            "Searching 7 job boards for React developer positions", "success", 5000
        )
        
        self.log_activity(
            "job-searcher-agent", "job_search", "Jobs Found",
            "Found 15 matching positions, filtered to 3 top matches", "success", 2500
        )
        
        time.sleep(1)
        
        # Simulate cover letter generator activities
        self.log_activity(
            "cover-letter-generator", "cover_letter", "Cover Letter Generated",
            "Created personalized cover letter for TechFlow Inc position", "success", 3000
        )
        
        self.log_activity(
            "cover-letter-generator", "cover_letter", "Multiple Variants Created",
            "Generated 3 variants: professional, creative, technical", "success", 5500
        )
        
        time.sleep(1)
        
        # Simulate application workflow tracking
        app_id = f"app_{int(time.time())}"
        self.track_application_workflow(
            app_id, "Alex Johnson", "Senior Full Stack Developer", "TechFlow Inc",
            "resume_parsed", {"skills_match": 90, "experience_match": 95}
        )
        
        time.sleep(0.5)
        
        self.track_application_workflow(
            app_id, "Alex Johnson", "Senior Full Stack Developer", "TechFlow Inc",
            "jobs_found", {"matching_jobs": 3, "top_score": 90}
        )
        
        time.sleep(0.5)
        
        self.track_application_workflow(
            app_id, "Alex Johnson", "Senior Full Stack Developer", "TechFlow Inc",
            "cover_letters_generated", {"variants": 3, "word_count": 161}
        )
        
        # Record performance metrics
        self.record_performance_metric("resume_parse_time_ms", 1200, "resume-parser-agent")
        self.record_performance_metric("job_search_time_ms", 5000, "job-searcher-agent")
        self.record_performance_metric("cover_letter_gen_time_ms", 3000, "cover-letter-generator")
        self.record_performance_metric("skills_match_score", 90, "job-searcher-agent")
        
        print(f"\n✅ Simulated audit activities complete!")
    
    def run_demo(self):
        """Run auditor demo"""
        print(f"🚀 Starting Auditor Agent: {self.agent_name}")
        print("=" * 70)
        print("🔍 Specialization: Audit Trails & Transparency")
        print("🎯 Mission: Log all activities and provide accountability")
        print("=" * 70)
        
        print(f"\n🤖 Agent '{self.agent_name}' is now active!")
        print(f"\n🔄 This agent will:")
        print(f"   1. 📝 Log all agent activities and decisions")
        print(f"   2. 📋 Track application workflow progress")
        print(f"   3. 📊 Monitor system performance metrics")
        print(f"   4. 🔍 Provide audit trails for transparency")
        print(f"   5. 📈 Generate compliance and analytics reports")
        
        print(f"\n" + "=" * 70)
        print("🎬 DEMO: Audit and Transparency Process")
        print("=" * 70)
        
        # Simulate activities from other agents
        self.simulate_audit_activities()
        
        # Generate and display audit report
        print(f"\n📊 Generating Audit Report...")
        time.sleep(1)
        
        report = self.generate_audit_report(hours=1)  # Last hour
        self.display_audit_report(report)
        
        print(f"\n💾 Audit data saved to: {self.db_path}")
        print(f"🔍 Database contains:")
        
        # Show database statistics
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM audit_logs")
            audit_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM performance_metrics")
            metrics_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM application_workflow")
            workflow_count = cursor.fetchone()[0]
            
            conn.close()
            
            print(f"   📝 {audit_count} audit log entries")
            print(f"   📊 {metrics_count} performance metrics")
            print(f"   📋 {workflow_count} application workflows")
            
        except Exception as e:
            print(f"❌ Failed to query database stats: {e}")
        
        print(f"\n✅ Audit process complete! System is transparent and accountable.")
        
        # Check if running in demo mode
        if '--demo' in sys.argv:
            print("🎯 Demo mode: Exiting after audit report")
            print(f"👋 Auditor Agent '{self.agent_name}' demo completed!")
            return
            
        print(f"📡 Agent running... Press Ctrl+C to stop")
        
        # Keep agent alive for production
        try:
            while True:
                time.sleep(60)  # Check every minute
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔍 Auditor Agent monitoring...")
        except KeyboardInterrupt:
            print(f"\n\n👋 Auditor Agent '{self.agent_name}' shutting down...")
            print("✅ All audit data saved successfully!")

def main():
    if len(sys.argv) < 2:
        print("Usage: python auditor-agent.py <agent_name> [--demo]")
        print("Example: python auditor-agent.py audit-guardian")
        print("Example: python auditor-agent.py audit-guardian --demo")
        print()
        print("Options:")
        print("  --demo    Run once and exit (for testing)")
        print("  (none)    Run continuously (for production)")
        sys.exit(1)
    
    agent_name = sys.argv[1]
    agent = AuditorAgent(agent_name)
    agent.run_demo()

if __name__ == "__main__":
    main()