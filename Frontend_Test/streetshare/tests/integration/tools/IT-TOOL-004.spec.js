import { mount } from '@vue/test-utils';
import ToolCreate from '@/components/PopUp/ToolCreate.vue';

vi.mock('vue-toast-notification', () => ({ useToast: () => ({ error: vi.fn(), success: vi.fn() }) }));

describe('IT-TOOL-004', () => {
  it('calculates a lower deposit for Defekt than for Neu', async () => {
    const wrapper = mount(ToolCreate, {
      props: {
        showModal: true,
        newTool: { name: '', description: '', base_price: 100, tool_condition: 'Neu', deposit: 0 },
        usageFactor: { Neu: 0.35, 'Minimal abgenutzt': 0.3, Gebraucht: 0.25, 'Gut abgenutzt': 0.2, Defekt: 0.1 },
        week_multiplier: 1,
        toolStore: { createTool: vi.fn() },
      },
    });

    await wrapper.get('[data-test="tool-price"]').setValue('100');
    await wrapper.get('[data-test="tool-condition"]').setValue('Neu');
    const neuDeposit = Number(wrapper.get('[data-test="tool-deposit"]').element.value);

    await wrapper.get('[data-test="tool-condition"]').setValue('Defekt');
    const defektDeposit = Number(wrapper.get('[data-test="tool-deposit"]').element.value);

    expect(defektDeposit).toBeLessThan(neuDeposit);
  });
});
