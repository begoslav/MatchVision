"""Summary generation service for match summaries"""
import logging

logger = logging.getLogger(__name__)

class SummaryService:
    """Service for generating match summaries from statistics"""
    
    SUMMARY_TEMPLATES = {
        'dominant_win': [
            "Naprostá dominance {home_team}. {away_team} neměla šanci. Střely {home_shots}:{away_shots}, držení míče {home_possession}:{away_possession}%.",
            "{home_team} zcela přehrála {away_team}. Jasné vítězství s třemi góly rozdílu a výraznou převahou.",
            "Bez diskuse {home_team}. Efektivita střel a dominance ve všech aspektech hry. {away_team} rezignovala.",
        ],
        'narrow_win': [
            "{home_team} vítězí těsně 1:0 po dramatickém zápase. {away_team} si vytvořila příležitosti, ale chybělo konkrétní zakončení.",
            "Tesný výsledek rozhoduje jeden gól. {home_team} byla efektivnější před bránou. Zápas byl vyrovnaný, ale {home_team} si výhru zasloužila.",
            "Minimální marže vítězství pro {home_team}. Vyrovnný zápas rozhodla kvalita v útoku. {away_team} měla možnosti, ale neurvala je.",
        ],
        'draw': [
            "Vyrovnaný souboj bez vítěze. Obě mužstva si vytvořila příležitosti, ale jejich realizace se nepovedla. Spravedlivý результат.",
            "{home_team} a {away_team} se rozdělily o body. Zajímavý zápas s příležitostmi na obou stranách.",
            "Bez ideálního zakončení se zápas skončil v remíze. Oba týmy měly své příležitosti, ale střelecky nebyli přesní.",
        ],
        'home_loss': [
            "Překvapení! {away_team} zvítězila na hřišti {home_team}. Rozhodla kvalita v útoku a lépe využité příležitosti.",
            "Zklamání pro {home_team}. {away_team} se prosadila také díky slabší obraně domácích.",
            "{away_team} si odvážela vítězství. {home_team} nebyla dostatečně efektivní a defenzíva se zapomněla.",
        ]
    }
    
    @staticmethod
    def generate_match_summary(match_data: dict) -> str:
        """Generate match summary from match statistics"""
        try:
            # Extract basic data
            home_team = match_data.get('teams', {}).get('home', {}).get('name', 'Domácí')
            away_team = match_data.get('teams', {}).get('away', {}).get('name', 'Hosté')
            home_score = match_data.get('goals', {}).get('home', 0)
            away_score = match_data.get('goals', {}).get('away', 0)
            
            # Extract statistics if available
            statistics = match_data.get('statistics', [])
            home_stats_list = statistics[0].get('statistics', []) if len(statistics) > 0 else []
            away_stats_list = statistics[1].get('statistics', []) if len(statistics) > 1 else []

            # Build lookup dicts from [{type, value}] format
            home_stats = {s['type']: s['value'] for s in home_stats_list}
            away_stats = {s['type']: s['value'] for s in away_stats_list}

            def _int(val):
                if val is None:
                    return 0
                return int(str(val).replace('%', '') or 0)

            home_shots = _int(home_stats.get('Shots Total', home_stats.get('Total Shots', 0)))
            away_shots = _int(away_stats.get('Shots Total', away_stats.get('Total Shots', 0)))
            home_possession = _int(home_stats.get('Ball Possession', 50))
            away_possession = _int(away_stats.get('Ball Possession', 50))
            
            # Determine match type and get template
            summary = SummaryService._get_summary_from_stats(
                home_team, away_team, home_score, away_score,
                home_shots, away_shots, home_possession, away_possession
            )
            
            return summary
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            return "Zápas se odehrál dle plánu. Podrobné statistiky najdete výše."
    
    @staticmethod
    def _get_summary_from_stats(home_team: str, away_team: str, home_score: int,
                                away_score: int, home_shots: int, away_shots: int,
                                home_possession: float, away_possession: float) -> str:
        """Get summary based on match statistics"""
        
        # Determine match type
        goal_diff = home_score - away_score
        shot_diff = home_shots - away_shots
        possession_diff = home_possession - away_possession
        
        # Win/Draw/Loss with dominance
        if home_score > away_score:
            if goal_diff >= 3 or (shot_diff >= 5 and possession_diff > 15):
                category = 'dominant_win'
            else:
                category = 'narrow_win'
        elif home_score < away_score:
            category = 'home_loss'
        else:
            category = 'draw'
        
        # Get random template
        import random
        template = random.choice(SummaryService.SUMMARY_TEMPLATES[category])
        
        # Format template with actual data
        summary = template.format(
            home_team=home_team,
            away_team=away_team,
            home_score=home_score,
            away_score=away_score,
            home_shots=home_shots,
            away_shots=away_shots,
            home_possession=int(home_possession),
            away_possession=int(away_possession)
        )
        
        return summary
    
    @staticmethod
    def generate_team_form_summary(last_matches: list) -> dict:
        """Generate team form summary from last matches"""
        if not last_matches or len(last_matches) == 0:
            return {'wins': 0, 'draws': 0, 'losses': 0, 'goals_for': 0, 'goals_against': 0}
        
        stats = {'wins': 0, 'draws': 0, 'losses': 0, 'goals_for': 0, 'goals_against': 0}
        
        for match in last_matches[:5]:  # Last 5 matches
            try:
                home_score = match.get('goals', {}).get('home', 0)
                away_score = match.get('goals', {}).get('away', 0)
                team_is_home = match.get('teams', {}).get('home', {}).get('id')
                
                if home_score > away_score:
                    if team_is_home:
                        stats['wins'] += 1
                        stats['goals_for'] += home_score
                        stats['goals_against'] += away_score
                    else:
                        stats['losses'] += 1
                        stats['goals_for'] += away_score
                        stats['goals_against'] += home_score
                elif home_score < away_score:
                    if team_is_home:
                        stats['losses'] += 1
                        stats['goals_for'] += home_score
                        stats['goals_against'] += away_score
                    else:
                        stats['wins'] += 1
                        stats['goals_for'] += away_score
                        stats['goals_against'] += home_score
                else:
                    stats['draws'] += 1
                    stats['goals_for'] += home_score
                    stats['goals_against'] += away_score
            except Exception as e:
                logger.error(f"Error processing match: {str(e)}")
                continue
        
        return stats

# Create singleton instance
summary_service = SummaryService()
