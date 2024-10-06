using Microsoft.AspNetCore.Mvc.RazorPages;
using RacingRules.Services;

namespace RacingRules.Views.Racing;

public class Leaderboard : PageModel
{
    public Leaderboard(List<LeaderboardEntry>? leaderboardEntries)
    {
        LeaderboardEntries = leaderboardEntries;
    }

    public List<LeaderboardEntry>? LeaderboardEntries { get; }
}