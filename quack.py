import argparse
import duckdb
import pygame

conversions_sql = '''
INSERT INTO accounts
with conversions as (
  select min(event_ts) as event_ts, organization_id from mdw.main.events
  where event_name='org_updated_payment_method'
  group by all
), 
conversions_and_orgs as (
select CO.id as organization_id,
  friendly_name,
  organization_type,
  CO.created_ts,
  CO.free_trial_end_date,
  C.event_ts as upgrade_date
  from mdw.current_organizations CO
  join conversions C on C.organization_id = CO.id
)
SELECT organization_id as org_id,
       friendly_name as org_name,
       upgrade_date as convert_ts
       FROM conversions_and_orgs
      WHERE organization_id not in (SELECT DISTINCT org_id FROM accounts)
'''

create_table_sql = '''
CREATE TABLE IF NOT EXISTS accounts (
         org_id UUID,
         org_name VARCHAR,
         convert_ts TIMESTAMP)
'''

parser = argparse.ArgumentParser()
parser.add_argument('sound_file')
args = parser.parse_args()

con = duckdb.connect('local.duckdb')
# Create the local accounts table if it doesn't exist
con.sql(create_table_sql)

con.sql("attach 'md:'")

results = con.execute(conversions_sql).fetchone()[0]
print(f'Found {results} new customers')
pygame.init()
sound = pygame.mixer.Sound(args.sound_file)
for _ in range(results):
  # New user found, play that quack!
  channel = sound.play()
  while channel.get_busy():
    pygame.time.wait(100)

