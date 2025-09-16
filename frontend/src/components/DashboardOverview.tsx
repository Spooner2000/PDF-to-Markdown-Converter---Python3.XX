import {
  Alert,
  Badge,
  Card,
  Group,
  Loader,
  ScrollArea,
  SimpleGrid,
  Stack,
  Table,
  Text,
  ThemeIcon,
  Title
} from '@mantine/core';
import { IconAlertCircle, IconCheck, IconHeartbeat, IconTopologyFull } from '@tabler/icons-react';
import { DashboardSummary } from '../store/dashboard';

interface DashboardOverviewProps {
  summary?: DashboardSummary;
  routines: any[];
  devices: any[];
  notifications: any[];
  loading: boolean;
  events: { id: string; type: string; payload: Record<string, unknown>; timestamp: string }[];
}

const HEALTH_COLORS: Record<string, string> = {
  healthy: 'green',
  warning: 'yellow',
  critical: 'red',
  unknown: 'gray'
};

export function DashboardOverview({ summary, routines, devices, notifications, loading, events }: DashboardOverviewProps) {
  if (loading) {
    return (
      <Group justify="center" align="center" h="100%">
        <Loader color="blue" size="lg" />
      </Group>
    );
  }

  if (!summary) {
    return (
      <Alert color="yellow" title="Keine Daten" icon={<IconAlertCircle size={16} />}>
        Noch keine Daten geladen. Bitte aktualisieren oder erneut anmelden.
      </Alert>
    );
  }

  const countEntries = Object.entries(summary.counts ?? {});

  return (
    <Stack gap="md">
      <SimpleGrid cols={{ base: 1, sm: 2, lg: 4 }}>
        {countEntries.map(([key, value]) => (
          <Card key={key} withBorder>
            <Stack gap={4}>
              <Text size="sm" c="dimmed" tt="uppercase">
                {key.replace('_', ' ')}
              </Text>
              <Title order={2}>{value}</Title>
            </Stack>
          </Card>
        ))}
        <Card withBorder>
          <Stack gap={6}>
            <Group gap={8}>
              <ThemeIcon variant="light" color="teal" radius="xl">
                <IconHeartbeat size={18} />
              </ThemeIcon>
              <Text fw={600}>System Health</Text>
            </Group>
            <Group gap={8}>
              {Object.entries(summary.system_health ?? {}).map(([domain, state]) => (
                <Badge key={domain} color={HEALTH_COLORS[state] ?? 'gray'}>
                  {domain}: {state}
                </Badge>
              ))}
            </Group>
          </Stack>
        </Card>
      </SimpleGrid>

      <SimpleGrid cols={{ base: 1, xl: 2 }} spacing="lg">
        <Card withBorder>
          <Stack gap="sm">
            <Group justify="space-between">
              <Title order={4}>Aktive Routinen</Title>
              <Badge color="blue">{routines.length}</Badge>
            </Group>
            <ScrollArea h={220} offsetScrollbars>
              <Stack gap="sm">
                {routines.map((routine) => (
                  <Card key={routine.id} padding="sm" shadow="xs" radius="md">
                    <Group justify="space-between" align="flex-start">
                      <Stack gap={4}>
                        <Text fw={600}>{routine.name}</Text>
                        <Text size="sm" c="dimmed">
                          {routine.description ?? 'Keine Beschreibung'}
                        </Text>
                      </Stack>
                      <Badge color={routine.status === 'active' ? 'teal' : routine.status === 'paused' ? 'yellow' : 'gray'}>
                        {routine.status}
                      </Badge>
                    </Group>
                  </Card>
                ))}
              </Stack>
            </ScrollArea>
          </Stack>
        </Card>

        <Card withBorder>
          <Stack gap="sm">
            <Group justify="space-between">
              <Title order={4}>Geräte-Status</Title>
              <Badge color="violet">{devices.length}</Badge>
            </Group>
            <ScrollArea h={220} offsetScrollbars>
              <Stack gap="sm">
                {devices.map((device) => (
                  <Card key={device.id} padding="sm" radius="md">
                    <Group justify="space-between" align="center">
                      <Stack gap={2}>
                        <Text fw={600}>{device.name}</Text>
                        <Text size="sm" c="dimmed">
                          {device.device_type} • {device.connection?.host ?? 'Unbekannt'}
                        </Text>
                      </Stack>
                      <Badge color={HEALTH_COLORS[device.health] ?? 'gray'}>{device.health}</Badge>
                    </Group>
                  </Card>
                ))}
              </Stack>
            </ScrollArea>
          </Stack>
        </Card>
      </SimpleGrid>

      <SimpleGrid cols={{ base: 1, xl: 2 }} spacing="lg">
        <Card withBorder>
          <Title order={4} mb="sm">
            Letzte Log-Ereignisse
          </Title>
          <ScrollArea h={260} offsetScrollbars>
            <Table striped highlightOnHover>
              <Table.Thead>
                <Table.Tr>
                  <Table.Th>Zeit</Table.Th>
                  <Table.Th>Quelle</Table.Th>
                  <Table.Th>Level</Table.Th>
                  <Table.Th>Nachricht</Table.Th>
                </Table.Tr>
              </Table.Thead>
              <Table.Tbody>
                {(summary.recent_logs ?? []).map((log) => (
                  <Table.Tr key={log.id}>
                    <Table.Td>{new Date(log.timestamp).toLocaleTimeString()}</Table.Td>
                    <Table.Td>{log.source ?? log.category}</Table.Td>
                    <Table.Td>
                      <Badge color={HEALTH_COLORS[log.level] ?? 'blue'} variant="light">
                        {log.level}
                      </Badge>
                    </Table.Td>
                    <Table.Td>{log.message}</Table.Td>
                  </Table.Tr>
                ))}
              </Table.Tbody>
            </Table>
          </ScrollArea>
        </Card>

        <Card withBorder>
          <Title order={4} mb="sm">
            Echtzeit-Stream
          </Title>
          <ScrollArea h={260} offsetScrollbars>
            <Stack gap="sm">
              {events.map((event) => (
                <Card key={event.id} padding="sm" radius="md" withBorder>
                  <Group justify="space-between">
                    <Badge color="blue" leftSection={<IconTopologyFull size={14} />}>
                      {event.type}
                    </Badge>
                    <Text size="xs" c="dimmed">
                      {new Date(event.timestamp).toLocaleTimeString()}
                    </Text>
                  </Group>
                  <Text size="sm" mt={6}>
                    {JSON.stringify(event.payload)}
                  </Text>
                </Card>
              ))}
              {events.length === 0 && (
                <Alert color="gray" icon={<IconCheck size={14} />}>
                  Noch keine Echtzeit-Events empfangen.
                </Alert>
              )}
            </Stack>
          </ScrollArea>
        </Card>
      </SimpleGrid>

      <Card withBorder>
        <Title order={4} mb="sm">
          Benachrichtigungen
        </Title>
        <ScrollArea h={200} offsetScrollbars>
          <Stack gap="sm">
            {notifications.map((notification) => (
              <Alert
                key={notification.id}
                color={notification.severity === 'critical' ? 'red' : notification.severity === 'warning' ? 'yellow' : 'blue'}
                title={notification.title}
                icon={<IconAlertCircle size={16} />}
              >
                <Text size="sm">{notification.message}</Text>
              </Alert>
            ))}
            {notifications.length === 0 && (
              <Alert color="green" icon={<IconCheck size={16} />}>Alles ruhig – keine offenen Benachrichtigungen.</Alert>
            )}
          </Stack>
        </ScrollArea>
      </Card>
    </Stack>
  );
}
