namespace RacingRules.Services;

public class ParticipantsService
{
    public List<Participant> Participants { get; set; } = [];
    public List<LeaderboardEntry>? Leaderboard { get; set; } = null;
}