import { mount, flushPromises } from '@vue/test-utils';
import Main from '@/views/Main/Main.vue';

vi.mock('vue-toast-notification', () => ({ useToast: () => ({ success: vi.fn(), error: vi.fn() }) }));

const store = {
  filters: { name: '', city: '', zip: '', country: '' },
  countries: ['Österreich'],
  page: 1,
  perPage: 25,
  total: 60,
  totalPages: 3,
  loading: false,
  tools: [],
  fetchTools: vi.fn().mockResolvedValue(),
  changePerPage: vi.fn(),
};

vi.mock('@/store/toolsStore', () => ({ useToolsStore: () => store }));

describe('IT-TOOL-003', () => {
  beforeEach(() => {
    store.page = 1;
    store.fetchTools.mockClear();
  });

  it('changes the page and fetches new tools on pagination', async () => {
    const wrapper = mount(Main, {
      global: { stubs: { RequestCreate: true } },
    });

    await flushPromises();
    await wrapper.get('[data-test="pagination-next"]').trigger('click');
    await flushPromises();

    expect(store.page).toBe(2);
    expect(store.fetchTools).toHaveBeenCalled();
  });
});
