import { NavLink, ScrollArea, Stack, Text } from '@mantine/core';
import {
  IconApps,
  IconApi,
  IconDeviceDesktop,
  IconHome,
  IconServer,
  IconTerminal
} from '@tabler/icons-react';

type SidebarNavProps = {
  active: string;
  onChange: (view: string) => void;
};

const NAV_ITEMS = [
  { label: 'Übersicht', value: 'dashboard', icon: IconHome },
  { label: 'Routinen', value: 'routines', icon: IconApps },
  { label: 'Skripte', value: 'scripts', icon: IconTerminal },
  { label: 'Geräte', value: 'devices', icon: IconDeviceDesktop },
  { label: 'APIs', value: 'apis', icon: IconApi },
  { label: 'HTTP-Server', value: 'httpServers', icon: IconServer }
];

export function SidebarNav({ active, onChange }: SidebarNavProps) {
  return (
    <ScrollArea h="100%" p="md">
      <Stack gap="xs">
        <Text size="sm" c="dimmed" fw={600} tt="uppercase">
          Navigation
        </Text>
        {NAV_ITEMS.map((item) => (
          <NavLink
            key={item.value}
            label={item.label}
            leftSection={<item.icon size={16} />}
            active={active === item.value}
            onClick={() => onChange(item.value)}
          />
        ))}
      </Stack>
    </ScrollArea>
  );
}
