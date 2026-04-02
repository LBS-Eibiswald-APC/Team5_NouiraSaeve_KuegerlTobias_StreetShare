import { mount } from '@vue/test-utils';
import ToolCreate from '@/components/PopUp/ToolCreate.vue';

vi.mock('vue-toast-notification', () => ({ useToast: () => ({ success: vi.fn(), error: vi.fn() }) }));

describe('UT-TOOL-002', () => {
  it('contains all predefined condition options', () => {
    const wrapper = mount(ToolCreate, {
      props: {
        showModal: true,
        newTool: { name: '', description: '', base_price: 0, tool_condition: 'Neu', deposit: 0 },
        usageFactor: { Neu: 0.35, 'Minimal abgenutzt': 0.3, Gebraucht: 0.25, 'Gut abgenutzt': 0.2, Defekt: 0.1 },
        week_multiplier: 1,
        toolStore: { createTool: vi.fn() },
      },
    });

    const options = wrapper.findAll('option').map((o) => o.text());
    expect(options).toEqual(['Neu', 'Minimal abgenutzt', 'Gebraucht', 'Gut abgenutzt', 'Defekt']);
  });
});
