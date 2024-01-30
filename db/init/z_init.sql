INSERT INTO socialcampaigns.appuser VALUES
('IslabUnimi', 'password_ignored', TRUE);

INSERT INTO socialcampaigns.appuser VALUES
('VastProject', 'password_ignored', TRUE);

INSERT INTO socialcampaigns.appuser VALUES
('wittertest55555', 'password_ignored', TRUE);

INSERT INTO socialcampaigns.social_network VALUES (0, 'DUMMY');
INSERT INTO socialcampaigns.social_network VALUES (1, 'TWITTER');
INSERT INTO socialcampaigns.social_network VALUES (2, 'MASTODON');

INSERT INTO socialcampaigns.status VALUES
(1, 'Created'),
(2, 'Scheduled'),
(3, 'Published'),
(4, 'Deleted');

-- TWITTER

INSERT INTO socialcampaigns.setting VALUES
(1, 'IslabUnimi', 'api_key', ''),
(1, 'IslabUnimi', 'api_key_secret', ''),
(1, 'IslabUnimi', 'access_token', ''),
(1, 'IslabUnimi', 'access_token_secret', ''),
(1, 'IslabUnimi', 'client_ID', ''),
(1, 'IslabUnimi', 'client_Secret', ''),
(1, 'IslabUnimi', 'bearer_token', '');

INSERT INTO socialcampaigns.setting VALUES
(1, 'VastProject', 'api_key', ''),
(1, 'VastProject', 'api_key_secret', ''),
(1, 'VastProject', 'access_token', ''),
(1, 'VastProject', 'access_token_secret', ''),
(1, 'VastProject', 'client_ID', ''),
(1, 'VastProject', 'client_Secret', ''),
(1, 'VastProject', 'bearer_token', '');

INSERT INTO socialcampaigns.setting VALUES
(1, 'wittertest55555', 'api_key', ''),
(1, 'wittertest55555', 'api_key_secret', ''),
(1, 'wittertest55555', 'access_token', ''),
(1, 'wittertest55555', 'access_token_secret', ''),
(1, 'wittertest55555', 'client_ID', ''),
(1, 'wittertest55555', 'client_Secret', ''),
(1, 'wittertest55555', 'bearer_token', '');

-- MASTODON

INSERT INTO socialcampaigns.setting VALUES
(2, 'IslabUnimi', 'instance', ''),
(2, 'IslabUnimi', 'email', ''),
(2, 'IslabUnimi', 'password', ''),
(2, 'IslabUnimi', 'account_id', '');

