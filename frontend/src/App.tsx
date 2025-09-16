import { AppShell, Badge, Card, Group, ScrollArea, Stack, Table, Text } from '@mantine/core';
import { useEffect, useMemo, useState } from 'react';
import { AppHeader } from './components/AppHeader';
import { DashboardOverview } from './components/DashboardOverview';
import { LoginOverlay } from './components/LoginOverlay';
import { SidebarNav } from './components/SidebarNav';
import { useEventStream } from './hooks/useEventStream';
import { useDashboardStore } from './store/dashboard';
import { useSessionStore } from './store/session';

function RoutinesTable({ routines }: { routines: any[] }) {
  return (
    <Card withBorder>
      <ScrollArea h={520} offsetScrollbars>
        <Table striped highlightOnHover>
          <Table.Thead>
            <Table.Tr>
              <Table.Th>Name</Table.Th>
              <Table.Th>Status</Table.Th>
              <Table.Th>Trigger</Table.Th>
              <Table.Th>Owner</Table.Th>
            </Table.Tr>
          </Table.Thead>
          <Table.Tbody>
            {routines.map((routine) => (
              <Table.Tr key={routine.id}>
                <Table.Td>
                  <Stack gap={2}>
                    <Text fw={600}>{routine.name}</Text>
                    <Text size="sm" c="dimmed">
                      {routine.description ?? '—'}
                    </Text>
                  </Stack>
                </Table.Td>
                <Table.Td>
                  <Badge color={routine.status === 'active' ? 'teal' : routine.status === 'paused' ? 'yellow' : 'gray'}>
                    {routine.status}
                  </Badge>
                </Table.Td>
                <Table.Td>{routine.trigger?.type ?? '—'}</Table.Td>
                <Table.Td>{routine.owner ?? '—'}</Table.Td>
              </Table.Tr>
            ))}
          </Table.Tbody>
        </Table>
      </ScrollArea>
    </Card>
  );
}

function DevicesTable({ devices }: { devices: any[] }) {
  return (
    <Card withBorder>
      <ScrollArea h={520} offsetScrollbars>
        <Table striped highlightOnHover>
          <Table.Thead>
            <Table.Tr>
              <Table.Th>Name</Table.Th>
              <Table.Th>Typ</Table.Th>
              <Table.Th>Status</Table.Th>
              <Table.Th>Verbindung</Table.Th>
            </Table.Tr>
          </Table.Thead>
          <Table.Tbody>
            {devices.map((device) => (
              <Table.Tr key={device.id}>
                <Table.Td>{device.name}</Table.Td>
                <Table.Td>{device.device_type}</Table.Td>
                <Table.Td>
                  <Badge color={device.health === 'healthy' ? 'teal' : device.health === 'warning' ? 'yellow' : 'gray'}>
                    {device.health}
                  </Badge>
                </Table.Td>
                <Table.Td>{device.connection?.host ?? '—'}</Table.Td>
              </Table.Tr>
            ))}
          </Table.Tbody>
        </Table>
      </ScrollArea>
    </Card>
  );
}

function GenericTable({ items, title }: { items: any[]; title: string }) {
  return (
    <Card withBorder>
      <Text fw={600} mb="sm">
        {title}
      </Text>
      <ScrollArea h={520} offsetScrollbars>
        <Stack gap="sm">
          {items.map((item) => (
            <Card key={item.id} padding="sm" withBorder radius="md">
              <Stack gap={4}>
                <Text fw={600}>{item.name}</Text>
                <Text size="sm" c="dimmed">
                  {item.description ?? 'Keine Beschreibung'}
                </Text>
              </Stack>
            </Card>
          ))}
        </Stack>
      </ScrollArea>
    </Card>
  );
}

export default function App() {
  const { token, user, loading: authLoading, error, login, logout } = useSessionStore();
  const { summary, routines, devices, notifications, loading: dashboardLoading, refresh } = useDashboardStore();
  const [activeView, setActiveView] = useState('dashboard');
  const { events } = useEventStream(Boolean(token));

  useEffect(() => {
    if (token) {
      refresh(token);
    }
  }, [token, refresh]);

  const handleLogin = async (username: string, password: string) => {
    await login(username, password);
  };

  const handleRefresh = () => {
    if (token) {
      refresh(token);
    }
  };

  const content = useMemo(() => {
    if (!token) {
      return <LoginOverlay loading={authLoading} error={error} onSubmit={handleLogin} />;
    }

    if (activeView === 'dashboard') {
      return (
        <DashboardOverview
          summary={summary}
          routines={routines}
          devices={devices}
          notifications={notifications}
          loading={dashboardLoading}
          events={events}
        />
      );
    }

    if (activeView === 'routines') {
      return <RoutinesTable routines={routines} />;
    }

    if (activeView === 'devices') {
      return <DevicesTable devices={devices} />;
    }

    if (activeView === 'apis') {
      return <GenericTable items={summary?.api_services ?? []} title="API-Services" />;
    }

    if (activeView === 'httpServers') {
      return <GenericTable items={summary?.http_servers ?? []} title="HTTP-Server" />;
    }

    return <GenericTable items={summary?.scripts ?? []} title="Skripte" />;
  }, [token, activeView, summary, routines, devices, notifications, dashboardLoading, events, authLoading, error]);

  return (
    <AppShell
      header={{ height: 96 }}
      navbar={{ width: 260, breakpoint: 'lg', collapsed: { mobile: !token } }}
      padding="md"
    >
      <AppShell.Header>
        <AppHeader user={user} onLogout={logout} onRefresh={handleRefresh} />
      </AppShell.Header>
      <AppShell.Navbar>
        {token ? <SidebarNav active={activeView} onChange={setActiveView} /> : null}
      </AppShell.Navbar>
      <AppShell.Main>{content}</AppShell.Main>
    </AppShell>
  );
}
