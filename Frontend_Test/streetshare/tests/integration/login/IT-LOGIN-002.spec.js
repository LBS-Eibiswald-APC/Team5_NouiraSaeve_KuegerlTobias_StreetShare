import { mount } from '@vue/test-utils';
import MainNav from '@/components/MainNav.vue';

const push = vi.fn();
const logout = vi.fn();

vi.mock('vue-router', async () => {
  const actual = await vi.importActual('vue-router');
  return {
    ...actual,
    useRouter: () => ({ push }),
  };
});

vi.mock('@/store/authStore', () => ({
  useAuthStore: () => ({
    user: { first_name: 'Tobias', last_name: 'Kügerl' },
    getMe: vi.fn(),
    logout,
  }),
}));

describe('IT-LOGIN-002', () => {
  it('shows the user name in the main navigation after login', () => {
    const wrapper = mount(MainNav, {
      global: { stubs: ['ToggleTheme'] },
    });

    expect(wrapper.text()).toContain('Tobias Kügerl');
  });
});
