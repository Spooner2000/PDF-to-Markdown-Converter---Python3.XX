import { Button, Card, PasswordInput, Stack, Text, TextInput, Title } from '@mantine/core';
import { FormEvent, useState } from 'react';

interface LoginOverlayProps {
  loading: boolean;
  error?: string;
  onSubmit: (username: string, password: string) => Promise<void>;
}

export function LoginOverlay({ loading, error, onSubmit }: LoginOverlayProps) {
  const [username, setUsername] = useState('admin');
  const [password, setPassword] = useState('admin123');

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    await onSubmit(username, password);
  };

  return (
    <Stack align="center" justify="center" h="100%">
      <Card withBorder shadow="xl" padding="xl" maw={420} w="100%">
        <form onSubmit={handleSubmit}>
          <Stack gap="sm">
            <Title order={3} ta="center">
              Willkommen im Admin Dashboard
            </Title>
            <Text size="sm" c="dimmed" ta="center">
              Bitte melden Sie sich mit Ihren Zugangsdaten an, um auf Automationen und Monitoring zuzugreifen.
            </Text>
            <TextInput
              label="Benutzername"
              placeholder="admin"
              value={username}
              onChange={(event) => setUsername(event.currentTarget.value)}
              required
            />
            <PasswordInput
              label="Passwort"
              placeholder="•••••••"
              value={password}
              onChange={(event) => setPassword(event.currentTarget.value)}
              required
            />
            {error && (
              <Text size="sm" c="red" ta="center">
                {error}
              </Text>
            )}
            <Button type="submit" loading={loading} radius="md">
              Anmelden
            </Button>
          </Stack>
        </form>
      </Card>
    </Stack>
  );
}
