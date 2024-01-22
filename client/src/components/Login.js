import { useState } from "react";
import { Link } from "react-router-dom";

export default function Login({ setUser }) {
  const [loginInfo, setLoginInfo] = useState({ username: "", password: "" });

  const handleLoginChange = (e) => {
    setLoginInfo({ ...loginInfo, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    fetch("/sign_in", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(loginInfo),
    })
      .then((r) => r.json())
      .then((data) => {
        setUser(data);
      });
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="username">Username: </label>
          <input
            value={loginInfo.username}
            id="username"
            name="username"
            onChange={handleLoginChange}
          />
        </div>
        <div>
          <label htmlFor="password">Password: </label>
          <input
            onChange={handleLoginChange}
            value={loginInfo.password}
            type="password"
            id="password"
            name="password"
          />
          <div>
            <input type="submit" value="Login" />
          </div>
        </div>
      </form>
      <Link to="/signup">Sign Up</Link>
    </div>
  );
}
