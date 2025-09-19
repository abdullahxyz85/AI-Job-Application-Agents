import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
} from "react";
import { showToast } from "../components/Toast";

interface User {
  user_id: string;
  full_name: string;
  email: string;
  phone?: string;
  location?: string;
  experience_level: string;
  desired_salary?: string;
  preferred_job_types: string[];
  profile_picture?: string;
  resume_uploaded: boolean;
  skills: Array<{
    id: number;
    skill_name: string;
    proficiency_level: string;
    years_experience: number;
  }>;
  education: Array<{
    id: number;
    institution_name: string;
    degree: string;
    field_of_study?: string;
    start_date?: string;
    end_date?: string;
    gpa?: string;
    is_current: boolean;
  }>;
  work_experience: Array<{
    id: number;
    company_name: string;
    job_title: string;
    description?: string;
    start_date?: string;
    end_date?: string;
    is_current: boolean;
    salary?: string;
    location?: string;
  }>;
  created_at: string;
  updated_at: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  signIn: (email: string, password: string) => Promise<boolean>;
  signUp: (userData: SignUpData) => Promise<boolean>;
  signOut: () => void;
  updateProfile: (profileData: Partial<User>) => Promise<boolean>;
  refreshProfile: () => Promise<void>;
}

interface SignUpData {
  full_name: string;
  email: string;
  password: string;
  phone?: string;
  location?: string;
  experience_level?: string;
  desired_salary?: string;
  preferred_job_types?: string[];
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

const API_BASE_URL = "http://localhost:8000";

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  // Initialize authentication state
  useEffect(() => {
    const initializeAuth = async () => {
      const token = localStorage.getItem("access_token");
      if (token) {
        try {
          const response = await fetch(`${API_BASE_URL}/api/auth/me`, {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          });

          if (response.ok) {
            const data = await response.json();
            setUser(data.profile);
            setIsAuthenticated(true);
          } else {
            // Token is invalid
            localStorage.removeItem("access_token");
          }
        } catch (error) {
          console.error("Auth initialization error:", error);
          localStorage.removeItem("access_token");
        }
      }
      setIsLoading(false);
    };

    initializeAuth();
  }, []);

  const signIn = async (email: string, password: string): Promise<boolean> => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/signin`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem("access_token", data.access_token);
        await refreshProfile();
        setIsAuthenticated(true);
        showToast.success(`Welcome back!`);
        return true;
      } else {
        showToast.error(data.detail || "Login failed");
        return false;
      }
    } catch (error) {
      console.error("Sign in error:", error);
      showToast.error("Network error. Please try again.");
      return false;
    }
  };

  const signUp = async (userData: SignUpData): Promise<boolean> => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/signup`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(userData),
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem("access_token", data.access_token);
        await refreshProfile();
        setIsAuthenticated(true);
        showToast.success(`Welcome to AI Job Agent, ${userData.full_name}!`);
        return true;
      } else {
        showToast.error(data.detail || "Registration failed");
        return false;
      }
    } catch (error) {
      console.error("Sign up error:", error);
      showToast.error("Network error. Please try again.");
      return false;
    }
  };

  const signOut = () => {
    localStorage.removeItem("access_token");
    setUser(null);
    setIsAuthenticated(false);
    showToast.info("You have been signed out");
  };

  const updateProfile = async (
    profileData: Partial<User>
  ): Promise<boolean> => {
    try {
      const token = localStorage.getItem("access_token");
      if (!token) {
        throw new Error("No access token");
      }

      const response = await fetch(`${API_BASE_URL}/api/auth/profile`, {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(profileData),
      });

      if (response.ok) {
        await refreshProfile();
        showToast.success("Profile updated successfully");
        return true;
      } else {
        const data = await response.json();
        showToast.error(data.detail || "Failed to update profile");
        return false;
      }
    } catch (error) {
      console.error("Update profile error:", error);
      showToast.error("Failed to update profile");
      return false;
    }
  };

  const refreshProfile = async (): Promise<void> => {
    try {
      const token = localStorage.getItem("access_token");
      if (!token) {
        throw new Error("No access token");
      }

      const response = await fetch(`${API_BASE_URL}/api/auth/me`, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });

      if (response.ok) {
        const data = await response.json();
        setUser(data.profile);
      } else {
        throw new Error("Failed to fetch profile");
      }
    } catch (error) {
      console.error("Refresh profile error:", error);
      signOut();
    }
  };

  const value: AuthContextType = {
    user,
    isAuthenticated,
    isLoading,
    signIn,
    signUp,
    signOut,
    updateProfile,
    refreshProfile,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export default AuthProvider;
