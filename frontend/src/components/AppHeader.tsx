import { Avatar, Button, Group, Stack, Text, Title } from '@mantine/core';
import { IconLogout, IconRefresh } from '@tabler/icons-react';
import { UserProfile } from '../types/user';

type AppHeaderProps = {
  user?: UserProfile;
  onLogout: () => void;
  onRefresh: () => void;
};

export function AppHeader({ user, onLogout, onRefresh }: AppHeaderProps) {
  return (
    <Group justify="space-between" p="md">
      <Stack gap={2}>
        <Title order={3}>Admin Automation Dashboard Pro</Title>
        <Text size="sm" c="dimmed">
          Zentrale Steuerung für Routinen, Geräte, APIs und Server mit Echtzeit-Insights
        </Text>
      </Stack>
      <Group gap="sm">
        <Button variant="light" leftSection={<IconRefresh size={16} />} onClick={onRefresh}>
          Aktualisieren
        </Button>
        {user && (
          <Group gap="xs">
            <Avatar radius="xl" color="blue">
              {user.full_name
                .split(' ')
                .map((name) => name.charAt(0))
                .join('')
                .slice(0, 2)
                .toUpperCase()}
            </Avatar>
            <Stack gap={0}>
              <Text fw={600}>{user.full_name}</Text>
              <Text size="xs" c="dimmed">
                Rollen: {user.roles.join(', ')}
              </Text>
            </Stack>
          </Group>
        )}
        <Button color="red" variant="subtle" leftSection={<IconLogout size={16} />} onClick={onLogout}>
          Abmelden
        </Button>
      </Group>
    </Group>
  );
}
