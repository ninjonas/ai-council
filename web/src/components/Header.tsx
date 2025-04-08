import { UI_CONSTANTS } from "../constants";
import ThemeToggle from "./ThemeToggle";

const Header = () => {
  return (
    <header className="mb-8 text-center relative">
      <div className="absolute right-0 top-0">
        <ThemeToggle />
      </div>
      <h1 className="text-4xl font-bold mb-2" style={{ color: "var(--primary)" }}>
        {UI_CONSTANTS.TITLE}
      </h1>
      <p className="text-lg" style={{ color: "var(--text-secondary)" }}>
        {UI_CONSTANTS.SUBTITLE}
      </p>
    </header>
  );
};

export default Header;
