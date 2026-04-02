import { mount, flushPromises } from '@vue/test-utils';
import Main from '@/views/Main/Main.vue';

vi.mock('vue-toast-notification', () => ({ useToast: () => ({ success: vi.fn(), error: vi.fn() }) }));

const store = {
  filters: { name: '', city: '', zip: '', country: '' },
  countries: ['Österreich', 'Deutschland'],
  page: 1,
  perPage: 25,
  total: 2,
  totalPages: 1,
  loading: false,
  tools: [
    { id: 1, name: 'Bohrer Wien', tool_condition: 'Neu', deposit: 10, creator_city: 'Wien', creator_country: 'Österreich', creator_display_name: 'Anna' },
  ],
  fetchTools: vi.fn().mockResolvedValue(),
  changePerPage: vi.fn(),
};

vi.mock('@/store/toolsStore', () => ({ useToolsStore: () => store }));

describe('IT-TOOL-002', () => {
  beforeEach(() => {
    store.fetchTools.mockClear();
    store.filters.name = '';
    store.filters.city = '';
  });

  it('updates the tool list when filters change', async () => {
    const wrapper = mount(Main, {
      global: { stubs: { RequestCreate: true } },
    });

    await flushPromises();
    await wrapper.get('[data-test="filter-city"]').setValue('Wien');
    await wrapper.get('[data-test="filter-apply"]').trigger('click');
    await flushPromises();

    expect(store.filters.city).toBe('Wien');
    expect(store.fetchTools).toHaveBeenCalled();
  });
});
