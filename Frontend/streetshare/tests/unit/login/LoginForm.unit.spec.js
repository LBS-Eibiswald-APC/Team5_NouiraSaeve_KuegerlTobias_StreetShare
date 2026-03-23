// Automated Unit Test: FE-LGN-UT-A-001
import { render, screen } from '@testing-library/react';
import LoginForm from '../../../components/LoginForm';

describe('LoginForm unit tests', () => {
    test('renders LoginForm component', () => {
        render(<LoginForm />);
        const linkElement = screen.getByText(/login/i);
        expect(linkElement).toBeInTheDocument();
    });
});