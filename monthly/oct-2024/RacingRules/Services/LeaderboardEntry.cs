namespace RacingRules.Services;

public class LeaderboardEntry
{
    public LeaderboardEntry(string firstName, string lastName, TimeSpan timeForCompletion)
    {
        FirstName = firstName;
        LastName = lastName;
        TimeForCompletion = timeForCompletion;
    }

    public string FirstName { get; }
    public string LastName { get; }
    public TimeSpan TimeForCompletion { get; }
}