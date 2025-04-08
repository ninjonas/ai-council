import { UI_CONSTANTS } from "../constants";

const Header = () => {
  return (
    <header className="mb-8 text-center">
      <h1 className="text-4xl font-bold text-blue-700 mb-2">
        {UI_CONSTANTS.TITLE}
      </h1>
      <p className="text-lg text-gray-600">
        {UI_CONSTANTS.SUBTITLE}
      </p>
    </header>
  );
};

export default Header;
