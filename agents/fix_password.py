"""
Password Reset Utility
This script will reset the password for a user to fix authentication issues
"""

import sqlite3
import bcrypt
import sys

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception as e:
        print(f"Password verification error: {e}")
        return False

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect("ai_job_agent.db")
    conn.row_factory = sqlite3.Row
    return conn

def reset_password(email: str, new_password: str):
    """Reset password for a user"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT user_id, email, password_hash FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        
        if not user:
            print(f"❌ User with email {email} not found!")
            conn.close()
            return False
        
        print(f"🔍 Found user: {user['user_id']}")
        print(f"📧 Email: {user['email']}")
        print(f"🔒 Current hash: {user['password_hash'][:50]}...")
        
        # Test current password verification
        current_verification = verify_password(new_password, user['password_hash'])
        print(f"🧪 Current password verification: {current_verification}")
        
        # Generate new hash
        new_hash = hash_password(new_password)
        print(f"🔄 New hash: {new_hash[:50]}...")
        
        # Test new hash verification
        new_verification = verify_password(new_password, new_hash)
        print(f"✅ New password verification: {new_verification}")
        
        if not new_verification:
            print("❌ New password hashing failed! Something is wrong with bcrypt.")
            conn.close()
            return False
        
        # Update password in database
        cursor.execute("UPDATE users SET password_hash = ? WHERE email = ?", (new_hash, email))
        conn.commit()
        
        print(f"✅ Password reset successful for {email}!")
        
        # Verify the update worked
        cursor.execute("SELECT password_hash FROM users WHERE email = ?", (email,))
        updated_user = cursor.fetchone()
        final_verification = verify_password(new_password, updated_user['password_hash'])
        print(f"🔬 Final verification: {final_verification}")
        
        conn.close()
        return final_verification
        
    except Exception as e:
        print(f"❌ Error resetting password: {e}")
        return False

def list_users():
    """List all users in the database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT user_id, full_name, email, created_at FROM users")
        users = cursor.fetchall()
        
        print("👥 Users in database:")
        print("-" * 60)
        for user in users:
            print(f"ID: {user['user_id']}")
            print(f"Name: {user['full_name']}")
            print(f"Email: {user['email']}")
            print(f"Created: {user['created_at']}")
            print("-" * 60)
        
        conn.close()
        return len(users)
        
    except Exception as e:
        print(f"❌ Error listing users: {e}")
        return 0

def main():
    print("🔧 Password Reset Utility")
    print("=" * 40)
    
    # List users first
    user_count = list_users()
    
    if user_count == 0:
        print("No users found in database.")
        return
    
    # Reset password for your email
    email = "abdullahxyz85@gmail.com"
    new_password = input(f"\n🔑 Enter new password for {email}: ").strip()
    
    if not new_password:
        print("❌ Password cannot be empty!")
        return
    
    success = reset_password(email, new_password)
    
    if success:
        print(f"\n🎉 Success! You can now sign in with:")
        print(f"📧 Email: {email}")
        print(f"🔑 Password: {new_password}")
        print("\n🚀 Try signing in again!")
    else:
        print("\n❌ Password reset failed. Check the error messages above.")

if __name__ == "__main__":
    main()